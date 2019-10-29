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

    def convert_bulletdata_to_nonpygame_data(self,tanks):
        bullets = []
        for tank in tanks:
            current = tanks[tank]['tank']
            for key in current.bullets:
                bullet = current.bullets[key]['bullet']
                dic = {'id':bullet.id,'pos':bullet.pos,'vel':bullet.vel}
                bullets.append(dic) 
        return bullets
            



