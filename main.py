import virtual_assistant as lisa
import reader

while True:
    data = lisa.listen()
    data = data.lower().split(" ")
    print(data)
    
    if (("hi" or "hello" or "hey") and "lisa") in data:
        lisa.respond("greetings")
        
    if (("start" and "scanning") or ("document" and "scan")) in data:
        lisa.respond("ack")
        reader.read()

    if (("get" or "retrieve" or "read") and ("last") and ("document")) in data:
        lisa.respond("ack")
        reader.read_again("recent1")
   
