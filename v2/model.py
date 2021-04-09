from sqlalchemy import create_engine, text

engine = create_engine('postgresql://jackson:password@localhost:5431/demo_stack')

with engine.connect() as conn:
  result = conn.execute(text('select * from test'))
  print(result.all())