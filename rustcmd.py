import asyncio
from rustplus import RustSocket, CommandOptions, Command, ServerDetails, ChatCommand,convert_coordinates
from rustplus import EntityEventPayload, TeamEventPayload, ChatEventPayload, ProtobufEvent, ChatEvent, EntityEvent, TeamEvent


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
async def gery(command: ChatCommand):
    await socket.send_team_message(f"Gergő, picit...")
  
  
@Command(server_details)
async def markers(command: ChatCommand):
    items = await socket.get_markers()
    for item in items:
        if item.type == 3:
            for order in item.sell_orders:
               await socket.send_team_message(f'{order.item_id}-{order.quantity}-{order.currency_id}-{order.cost_per_item}')
          
@EntityEvent(server_details, 21318704)
async def alarm(event: EntityEventPayload):
    await socket.send_team_message(f"{event.capacity}")



async def main():
    await socket.connect()
    info = await socket.get_info()  
    team_info = await socket.get_team_info()
    old_team = team_info.members
    
    while True:
        await asyncio.sleep(5)
        team_info = await socket.get_team_info()
        new_team = team_info.members
        for player in range(len(team_info.members)):
            if old_team[player].is_alive and not new_team[player].is_alive:
                await socket.send_team_message(f"{new_team[player].name} is dead in {convert_coordinates((old_team[player].x, old_team[player].y), info.size)}")
            if old_team[player].is_online and not new_team[player].is_online:
                await socket.send_team_message(f"{new_team[player].name} disconnected in {convert_coordinates((old_team[player].x, old_team[player].y), info.size)}")
            if not old_team[player].is_online and new_team[player].is_online:
                await socket.send_team_message(f"{new_team[player].name} connected in {convert_coordinates((old_team[player].x, old_team[player].y), info.size)}")          
        old_team = new_team
        await asyncio.sleep(1) 

if __name__ == "__main__":
    asyncio.run(main())
