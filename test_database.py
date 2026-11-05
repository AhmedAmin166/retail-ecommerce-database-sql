import sqlite3
import os
import sys

# Ensure UTF-8 output encoding for Windows command line
if sys.platform.startswith('win'):
    try:
        sys.stdout.reconfigure(encoding='utf-8')
    except AttributeError:
        pass

def run_project_test():
    base_dir = os.path.dirname(os.path.abspath(__file__))
    db_path = os.path.join(base_dir, "retail_analytics.db")

    if os.path.exists(db_path):
        os.remove(db_path)

    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    print("=================================================================")
    print("🚀 INITIALIZING DATABASE & RUNNING AUTOMATED AUDIT")
    print("=================================================================")

    # 1. Execute Schema
    schema_path = os.path.join(base_dir, "01_schema.sql")
    with open(schema_path, "r", encoding="utf-8") as f:
        schema_sql = f.read()
    cursor.executescript(schema_sql)
    print("✅ Step 1: 01_schema.sql executed successfully (Tables, Constraints, Indexes & Views).")

    # 2. Execute Seed Data
    seed_path = os.path.join(base_dir, "02_seed_data.sql")
    with open(seed_path, "r", encoding="utf-8") as f:
        seed_sql = f.read()
    cursor.executescript(seed_sql)
    conn.commit()
    print("✅ Step 2: 02_seed_data.sql executed successfully (Data Seeded).")

    # Verify Counts
    tables = ['categories', 'customers', 'products', 'inventory', 'orders', 'order_items', 'returns']
    print("\n📊 Table Record Counts:")
    for t in tables:
        cursor.execute(f"SELECT COUNT(*) FROM {t}")
        count = cursor.fetchone()[0]
        print(f"   - {t:<15}: {count} rows")

    # 3. Read and execute business queries
    queries_path = os.path.join(base_dir, "03_business_queries.sql")
    with open(queries_path, "r", encoding="utf-8") as f:
        queries_content = f.read()

    # Split by semicolon and clean lines
    raw_chunks = queries_content.split(';')
    raw_queries = []
    for chunk in raw_chunks:
        # Strip comments to see if actual SQL statement exists
        code_lines = [l for l in chunk.split('\n') if not l.strip().startswith('--')]
        clean_stmt = "\n".join(code_lines).strip()
        if clean_stmt:
            raw_queries.append(clean_stmt)

    query_titles = [
        "Query 1: Executive Financial KPI Dashboard",
        "Query 2: Product Performance, Profitability & Return Rate Analysis",
        "Query 3: Monthly Revenue Running Total & MoM Growth",
        "Query 4: RFM Customer Value Segmentation",
        "Query 5: Inventory Health & Reorder Restock Alert"
    ]

    print("\n=================================================================")
    print("💼 EXECUTING ADVANCED BUSINESS ANALYTICAL QUERIES")
    print("=================================================================")

    q_idx = 0
    for query in raw_queries:
        # filter out empty or comment-only chunks
        lines = [line for line in query.split('\n') if not line.strip().startswith('--')]
        clean_query = "\n".join(lines).strip()
        if not clean_query:
            continue
        
        title = query_titles[q_idx] if q_idx < len(query_titles) else f"Query {q_idx+1}"
        print(f"\n--- {title} ---")
        try:
            cursor.execute(clean_query)
            columns = [desc[0] for desc in cursor.description]
            rows = cursor.fetchall()

            # Format simple table
            col_widths = [max(len(col), max((len(str(row[i])) for row in rows), default=0)) for i, col in enumerate(columns)]
            header = " | ".join(f"{col:<{col_widths[i]}}" for i, col in enumerate(columns))
            separator = "-+-".join("-" * col_widths[i] for i in range(len(columns)))
            print(header)
            print(separator)
            for row in rows:
                print(" | ".join(f"{str(row[i]):<{col_widths[i]}}" for i, col in enumerate(columns)))
            q_idx += 1
        except Exception as e:
            print(f"❌ Error in query {q_idx+1}: {e}")
            sys.exit(1)

    conn.close()
    print("\n=================================================================")
    print("🎯 ALL AUDIT TESTS & QUERIES PASSED WITH ZERO ERRORS!")
    print(f"Database successfully saved to: {db_path}")
    print("=================================================================")

if __name__ == "__main__":
    run_project_test()
