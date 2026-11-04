import 'dart:convert';
import 'dart:io';

import 'package:drift/native.dart';
import 'package:flutter_test/flutter_test.dart';
import 'package:majestic_storage/majestic_storage.dart';
import 'package:sqlite3/sqlite3.dart' as sqlite;

// Run from App-Template with the pinned SDK. This qualification fixture changes
// no application source or host disk capacity: SQLite's page budget induces a
// real SQLITE_FULL inside its native encrypted engine.
void main() {
  test('native encrypted SQLITE_FULL keeps the prior record and recovers on restart', () async {
    final directory = await Directory.systemTemp.createTemp(
      'majestic-full-contract-',
    );
    final file = File('${directory.path}/records.sqlite');
    final key = List<int>.generate(32, (i) => i + 1);
    final raw = sqlite.sqlite3.open(file.path);
    configureEncryptedDatabase(raw, key);
    raw.execute('PRAGMA journal_mode = DELETE');
    final store = EncryptedDocumentStore(
      executor: NativeDatabase.opened(raw),
      appId: 'qa.storage-full',
      tableName: 'records',
    );
    const original = '{"id":"stable-record","value":"kept"}';
    try {
      await store.write('snapshot', original);
      final pages = raw.select('PRAGMA page_count').single.values.single as int;
      raw.execute('PRAGMA max_page_count = $pages');
      await expectLater(
        store.write(
          'snapshot',
          jsonEncode({'id': 'stable-record', 'value': 'x' * (1024 * 1024)}),
        ),
        throwsA(
          isA<sqlite.SqliteException>().having(
            (e) => e.resultCode,
            'SQLITE_FULL',
            13,
          ),
        ),
      );
      expect(await store.read('snapshot'), original);
    } finally {
      await store.close();
    }
    final reopened = EncryptedDocumentStore(
      executor: openEncryptedDatabase(file: file, key: key),
      appId: 'qa.storage-full',
      tableName: 'records',
    );
    try {
      expect(await reopened.read('snapshot'), original);
      await reopened.write(
        'snapshot',
        '{"id":"stable-record","value":"retry succeeded"}',
      );
      expect(await reopened.read('snapshot'), contains('retry succeeded'));
    } finally {
      await reopened.close();
    }
    expect(
      (await file.readAsBytes()).take(16).toList(),
      isNot(utf8.encode('SQLite format 3\u0000')),
    );
    final unkeyed = sqlite.sqlite3.open(
      file.path,
      mode: sqlite.OpenMode.readOnly,
    );
    try {
      expect(
        () => unkeyed.select('SELECT * FROM sqlite_master'),
        throwsA(isA<sqlite.SqliteException>()),
      );
    } finally {
      unkeyed.close();
      await directory.delete(recursive: true);
    }
  });
}
