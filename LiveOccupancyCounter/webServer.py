import os

def webserver(port=8001,folder='/public/'):
    os.chdir(os.getcwd()+folder)
    os.system('python3 -m http.server %d --bind 127.0.0.1' % port)

    return


