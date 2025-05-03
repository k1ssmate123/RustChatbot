import asyncio
from rustplus import RustSocket, CommandOptions, Command, ServerDetails, ChatCommand,convert_coordinates

options = CommandOptions(prefix="!")  # Command prefix
server_details = ServerDetails("168.100.161.91", "28082", 76561198882738407, 1711501874)
socket = RustSocket(server_details, command_options=options)

@Command(server_details)
async def hi(command: ChatCommand):
    await socket.send_team_message(f"Hi, {command.sender_name}")

@Command(server_details)
async def t(command: ChatCommand):
    await socket.send_team_message(f"Time is {(await socket.get_time()).time}")

@Command(server_details)
async def p(command: ChatCommand):
    await socket.send_team_message(f"Player count is:  {(await socket.get_info()).players}")

@Command(server_details)
async def tlm(command: ChatCommand):
    await socket.send_team_message(f"Player count is:  {(await socket.get_info()).players}")
    await socket.promote_to_team_leader(76561198882738407)
  
@Command(server_details)
async def markers(command: ChatCommand):
    items = await socket.get_markers()
    for item in items:
        if item.id == 3:
            await socket.send_team_message(f"{item.id}")
          
    

async def watch_death():
    team_info = await socket.get_team_info()
    for teammate in team_info.members:
        if not teammate.is_alive:
            sdata = await socket.get_info()
            await socket.send_team_message(f"{teammate.name} died at: {convert_coordinates((teammate.x,teammate.y), sdata.size)}")
            break
    await asyncio.sleep(2)  





async def main():
    await socket.connect()
    while True:
        await asyncio.sleep(1) 

if __name__ == "__main__":
    asyncio.run(main())
