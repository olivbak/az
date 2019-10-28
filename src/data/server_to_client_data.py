class server_to_client_data():
    def __init__(self):
        pass

    def convert_tankdata_to_nonpygame_data(self,tanks):
        data = []
        for tank in tanks:
            current = tanks[tank]['tank']
            dic = {'id':current.id,'pos':current.pos,'rotation':current.rotation}
            data.append(dic)
        return data
            
             



