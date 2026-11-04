#!/usr/bin/env python3
"""Fail-closed, dependency-free checks for the portfolio's main-only Actions policy.

The accepted YAML subset is block mappings/sequences, scalar values, flow scalar
lists and literal/folded blocks. YAML aliases, tags, merges, complex keys and flow
mappings (other than {}) are deliberately unsupported. Shell blocks are data,
not YAML. Unsupported syntax requires an explicit validator update, never a pass.
"""
from __future__ import annotations

import json
import re
from dataclasses import dataclass
from pathlib import Path
from typing import Any


class PolicySyntaxError(ValueError):
    """A workflow cannot be interpreted without ambiguity."""


@dataclass
class Line:
    indent: int
    body: str
    number: int


def _uncomment(value: str) -> str:
    quoted: str | None = None
    escaped = False
    for i, char in enumerate(value):
        if quoted == '"' and char == "\\" and not escaped:
            escaped = True
            continue
        if char in "\"'" and not escaped:
            if quoted == char:
                quoted = None
            elif quoted is None:
                quoted = char
        if char == "#" and quoted is None and (i == 0 or value[i - 1].isspace()):
            return value[:i].rstrip()
        escaped = False
    return value.rstrip()


def _scalar(value: str) -> Any:
    value = _uncomment(value).strip()
    if not value or value in {"null", "~"}:
        return None
    if value == "{}":
        return {}
    if value.startswith('"'):
        try:
            result = json.loads(value)
        except json.JSONDecodeError as error:
            raise PolicySyntaxError("unsupported quoted scalar") from error
        if not isinstance(result, str):
            raise PolicySyntaxError("expected a quoted scalar")
        return result
    if value.startswith("'"):
        if not re.fullmatch(r"'(?:[^']|'')*'", value):
            raise PolicySyntaxError("unsupported quoted scalar")
        return value[1:-1].replace("''", "'")
    if value.startswith("["):
        if not value.endswith("]"):
            raise PolicySyntaxError("unterminated flow list")
        inner = value[1:-1].strip()
        if not inner:
            return []
        # Flow lists are scalar pins, not arbitrary YAML expressions.
        items = re.findall(r"'(?:[^']|'')*'|\"(?:[^\"\\]|\\.)*\"|[^,]+", inner)
        if ",".join(items).replace(" ", "") != inner.replace(" ", ""):
            raise PolicySyntaxError("unsupported flow list")
        result = [_scalar(item.strip()) for item in items]
        if any(not isinstance(item, str) for item in result):
            raise PolicySyntaxError("flow list must contain only scalar strings")
        return result
    if value[0] in "&*!{]" or re.search(r"(?:^|\s)[&*][A-Za-z0-9_-]+", value):
        raise PolicySyntaxError("YAML anchors, aliases, tags and flow mappings are forbidden")
    return value


def _mapping_pair(body: str) -> tuple[str, str]:
    match = re.fullmatch(r"([A-Za-z_][\w.-]*|<<|'(?:[^']|'')*'|\"(?:[^\"\\]|\\.)*\"):\s*(.*)", body)
    if not match:
        raise PolicySyntaxError(f"unsupported YAML mapping: {body[:80]}")
    key, value = match.groups()
    key = _scalar(key)
    if not isinstance(key, str) or key == "<<":
        raise PolicySyntaxError("YAML merge keys are forbidden")
    return key, value


class _YamlSubset:
    def __init__(self, text: str):
        self.lines: list[Line] = []
        # Tabs inside run blocks are legal; reject them only in parsed YAML.
        for number, raw in enumerate(text.splitlines(), 1):
            if not raw.strip() or raw.lstrip().startswith("#"):
                continue
            indent = len(raw) - len(raw.lstrip(" "))
            self.lines.append(Line(indent, raw[indent:], number))
        self.position = 0

    def _value(self, raw: str, parent_indent: int) -> Any:
        raw = _uncomment(raw).strip()
        if re.fullmatch(r"[|>](?:[+-]?[1-9]?|[1-9][+-]?)", raw):
            block: list[str] = []
            while self.position < len(self.lines) and self.lines[self.position].indent > parent_indent:
                block.append(self.lines[self.position].body)
                self.position += 1
            return (" " if raw.startswith(">") else "\n").join(block)
        if raw:
            return _scalar(raw)
        if self.position < len(self.lines) and self.lines[self.position].indent > parent_indent:
            return self._node(self.lines[self.position].indent)
        return None

    def _node(self, indent: int) -> Any:
        sequence = self.lines[self.position].body.startswith("- ")
        output: Any = [] if sequence else {}
        while self.position < len(self.lines):
            line = self.lines[self.position]
            if line.indent < indent:
                break
            if line.indent != indent or "\t" in line.body:
                raise PolicySyntaxError(f"unsupported YAML indentation/tab at line {line.number}")
            self.position += 1
            if sequence:
                if not line.body.startswith("- "):
                    raise PolicySyntaxError("mixed YAML mapping and sequence")
                body = line.body[2:]
                if re.match(r"[\w.'\"-]+:\s", body) or body.endswith(":"):
                    key, value = _mapping_pair(body)
                    item = {key: self._value(value, indent + 2)}
                    if self.position < len(self.lines) and self.lines[self.position].indent > indent:
                        if self.lines[self.position].indent != indent + 2:
                            raise PolicySyntaxError("unsupported sequence mapping indentation")
                        more = self._node(indent + 2)
                        if not isinstance(more, dict) or set(item) & set(more):
                            raise PolicySyntaxError("duplicate sequence mapping key")
                        item.update(more)
                    output.append(item)
                else:
                    output.append(self._value(body, indent))
            else:
                key, value = _mapping_pair(line.body)
                if key in output:
                    raise PolicySyntaxError(f"duplicate YAML key: {key}")
                output[key] = self._value(value, indent)
        return output

    def parse(self) -> dict[str, Any]:
        if not self.lines or self.lines[0].indent:
            raise PolicySyntaxError("missing root YAML mapping")
        result = self._node(0)
        if self.position != len(self.lines) or not isinstance(result, dict):
            raise PolicySyntaxError("workflow must be one YAML mapping")
        return result


def parse_workflow(text: str) -> dict[str, Any]:
    """Parse the intentionally supported subset without YAML 1.1's on/boolean trap."""
    return _YamlSubset(text).parse()


_TOKEN = re.compile(r"\s*(\&\&|\|\||==|!=|<=|>=|[!<>()\[\],.]|'(?:[^']|'')*'|\"(?:[^\"\\]|\\.)*\"|[A-Za-z_][\w.-]*|[0-9]+(?:\.[0-9]+)?)")


class _Expression:
    def __init__(self, expression: str):
        self.tokens: list[str] = []
        position = 0
        while position < len(expression):
            match = _TOKEN.match(expression, position)
            if not match:
                raise PolicySyntaxError("unsupported job condition syntax")
            self.tokens.append(match.group(1))
            position = match.end()
        self.position = 0

    def _peek(self) -> str | None:
        return self.tokens[self.position] if self.position < len(self.tokens) else None

    def _take(self, wanted: str | None = None) -> str:
        value = self._peek()
        if value is None or (wanted and value != wanted):
            raise PolicySyntaxError("invalid job condition")
        self.position += 1
        return value

    def _primary(self) -> Any:
        if self._peek() == "!":
            self._take()
            return ("not", self._primary())
        if self._peek() == "(":
            self._take()
            value = self._or()
            self._take(")")
            return value
        token = self._take()
        if token[0] in "\"'":
            return ("literal", _scalar(token))
        if not re.fullmatch(r"[\w.-]+", token):
            raise PolicySyntaxError("invalid condition operand")
        value: Any = ("identifier", token)
        if self._peek() == "(":
            self._take()
            arguments = []
            while self._peek() != ")":
                arguments.append(self._or())
                if self._peek() != ",":
                    break
                self._take()
            self._take(")")
            value = ("call", token, tuple(arguments))
        return value

    def _compare(self) -> Any:
        value = self._primary()
        if self._peek() in {"==", "!=", "<", ">", "<=", ">="}:
            value = (self._take(), value, self._primary())
        return value

    def _and(self) -> Any:
        value = self._compare()
        while self._peek() == "&&":
            self._take()
            value = ("and", value, self._compare())
        return value

    def _or(self) -> Any:
        value = self._and()
        while self._peek() == "||":
            self._take()
            value = ("or", value, self._and())
        return value

    def parse(self) -> Any:
        result = self._or()
        if self.position != len(self.tokens):
            raise PolicySyntaxError("trailing job condition tokens")
        return result


def _equals(node: Any, identifier: str, literal: str) -> bool:
    return node in {
        ("==", ("identifier", identifier), ("literal", literal)),
        ("==", ("literal", literal), ("identifier", identifier)),
    }


def _allowed_events(node: Any) -> bool:
    if node[0] == "or":
        return _allowed_events(node[1]) and _allowed_events(node[2])
    return any(_equals(node, "github.event_name", event) for event in ("push", "workflow_dispatch"))


def _guarded(condition: Any) -> bool:
    if not isinstance(condition, str):
        return False
    expression = condition.strip()
    if expression.startswith("${{") and expression.endswith("}}"):
        expression = expression[3:-2].strip()
    try:
        parsed = _Expression(expression).parse()
    except PolicySyntaxError:
        return False

    def conjuncts(node: Any) -> list[Any]:
        return conjuncts(node[1]) + conjuncts(node[2]) if node[0] == "and" else [node]

    clauses = conjuncts(parsed)
    return (any(_equals(node, "github.ref", "refs/heads/main") for node in clauses)
            and any(_allowed_events(node) for node in clauses))


def _permissions(value: Any) -> bool:
    return isinstance(value, dict) and all(key == "contents" and isinstance(access, str) and access in {"read", "none"}
                                           for key, access in value.items())


def _immutable_use(value: Any) -> bool:
    """External executable tooling must resolve to an immutable source identity."""
    if not isinstance(value, str):
        return False
    if value.startswith("./"):
        parts = value[2:].split("/")
        return bool(parts) and all(re.fullmatch(r"[A-Za-z0-9_.-]+", part)
                                   and part not in {".", ".."} for part in parts)
    if value.startswith("docker://"):
        return bool(re.fullmatch(r"docker://[^@\s]+@sha256:[0-9a-f]{64}", value))
    return bool(re.fullmatch(r"[A-Za-z0-9_.-]+/[A-Za-z0-9_.-]+(?:/[A-Za-z0-9_.-]+)*@[0-9a-f]{40}", value))


def check_workflow(text: str) -> list[str]:
    """Return actionable policy violations; malformed/ambiguous YAML fails closed."""
    try:
        document = parse_workflow(text)
    except (PolicySyntaxError, TypeError, ValueError) as error:
        return [f"unsupported/ambiguous workflow YAML: {error}"]
    errors: list[str] = []
    events = document.get("on")
    if not isinstance(events, dict) or not events or set(events) - {"push", "workflow_dispatch"}:
        errors.append("only explicit main push and workflow_dispatch mappings are allowed")
    else:
        if "push" in events:
            push = events["push"]
            if (not isinstance(push, dict) or push.get("branches") != ["main"]
                    or set(push) - {"branches", "paths", "paths-ignore"}):
                errors.append("push must use branches: [main] without alternate branch/tag filters")
            elif "paths" in push and "paths-ignore" in push:
                errors.append("push cannot combine paths and paths-ignore")
        if "workflow_dispatch" in events and events["workflow_dispatch"] not in (None, {}):
            errors.append("workflow_dispatch must have no inputs or other configuration")
    if not _permissions(document.get("permissions")):
        errors.append("workflow permissions must explicitly allow at most contents: read")
    jobs = document.get("jobs")
    if not isinstance(jobs, dict) or not jobs:
        return errors + ["workflow must contain a nonempty jobs mapping"]
    for name, job in jobs.items():
        if not isinstance(job, dict):
            errors.append(f"job {name} must be an explicit mapping")
            continue
        if not _guarded(job.get("if")):
            errors.append(f"job {name} lacks mandatory main-ref and allowed-event execution guards")
        if "permissions" in job and not _permissions(job["permissions"]):
            errors.append(f"job {name} widens permissions beyond contents: read")
        if "uses" in job and not _immutable_use(job["uses"]):
            errors.append(f"job {name} reusable workflow must use an immutable 40-character commit")
        if "uses" in job and isinstance(job.get("with"), dict):
            if set(job["with"]) & {"ref", "repository", "branch", "sha"}:
                errors.append(f"job {name} cannot override reusable workflow code selection")
        steps = job.get("steps", [])
        if not isinstance(steps, list):
            errors.append(f"job {name} steps must be an explicit sequence")
            continue
        for step in steps:
            if not isinstance(step, dict):
                errors.append(f"job {name} contains an unsupported step")
                continue
            uses = step.get("uses", "")
            if "uses" in step and not _immutable_use(uses):
                errors.append(f"job {name} external action must use an immutable 40-character commit or Docker digest")
            if isinstance(uses, str) and uses.lower().startswith("actions/checkout@"):
                options = step.get("with", {})
                if not isinstance(options, dict) or set(options) & {"ref", "repository"}:
                    errors.append(f"job {name} has forbidden checkout ref/repository overrides")
    return sorted(set(errors))


def check_repository(repository: Path) -> list[str]:
    """Scan only active .github/workflows files, never archived copies."""
    errors: list[str] = []
    for workflow in sorted((repository / ".github/workflows").glob("*.y*ml")):
        errors.extend(f"{workflow.name}: {error}" for error in check_workflow(workflow.read_text()))
    return errors
