import os
import asyncio
import aiomysql
import ssl

from dotenv import load_dotenv
load_dotenv()

ctx = ssl.SSLContext(ssl.PROTOCOL_TLS_CLIENT)
ctx.load_verify_locations(cafile="cacert.pem")

loop = asyncio.get_event_loop()


async def connect_db():
   connection = await aiomysql.connect(
       host=os.getenv("HOST"),
       port=3306,
       user=os.getenv("USERNAME"),
       password=os.getenv("PASSWORD"),
       db=os.getenv("DATABASE"),
       loop=loop,
       ssl=ctx
   )
   cursor = await connection.cursor()
   await cursor.execute("select @@version")
   version = await cursor.fetchall()
   print('Running version: ', version)
   await cursor.close()
   connection.close()
loop.run_until_complete(connect_db())
