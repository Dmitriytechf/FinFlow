import psycopg2


print('=== Проверка миграции ===')

try:
    conn = psycopg2.connect(
        host='localhost',
        port=5433,
        user='finflow_user',
        password='finflow_pass',
        database='finflow_db'
    )
    
    cur = conn.cursor()
    
    # Проверяем таблицы
    cur.execute('''
        SELECT table_name 
        FROM information_schema.tables 
        WHERE table_schema = 'public'
        ORDER BY table_name;
    ''')
    
    tables = cur.fetchall()
    
    print(f'Таблиц создано: {len(tables)}')
    for table in tables:
        print(f'  - {table[0]}')

    # Проверяем что есть все нужные таблицы
    expected = {'users', 'accounts', 'categories', 'transactions', 'goals'}
    actual = {t[0] for t in tables}
    
    if expected.issubset(actual):
        print('\nВсе нужные таблицы созданы!')
    else:
        missing = expected - actual
        print(f'\nНе хватает таблиц: {missing}')

    # Проверяем структуру таблицы users
    # print("\nСтруктура таблицы 'users':")
    # cur.execute('''
    #     SELECT column_name, data_type, is_nullable
    #     FROM information_schema.columns 
    #     WHERE table_name = 'users'
    #     ORDER BY ordinal_position;
    # ''')
    
    # for col in cur.fetchall():
    #     nullable = 'NULL' if col[2] == 'YES' else 'NOT NULL'
    #     print(f'  - {col[0]}: {col[1]} ({nullable})')
    
    conn.close()
    
except Exception as e:
    print(f'Ошибка: {e}')
