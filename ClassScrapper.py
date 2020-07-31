from urllib.request import urlopen
import ssl
import os

class baseScrapper():

    @staticmethod
    def printdict(dictPDFs):
        for key, val  in dictPDFs.items():
            print(f'title: {key}')  
            print(f'link: {val}')

    @staticmethod
    def checkWithTxt(dictPDFs):
        for title, url in dictPDFs.items():
            with open('decretos.txt', 'a+') as fd:
                fd.write(f'{title}: {url}\n')
    
    @staticmethod
    def gotPDFs(dictPDFs, folder="Decretos_Covid"):
        '''
        gotPDFS as you can see for the name of this method the main functionality is got the PDF throw
        a request with a dictionary that has a link to do the request and the name of the PDF

        1.) do a contex to forgot the problem about the ssl certificate in the request 
        2.) create a folder in the current directory with the name that you want
        2.) then use a urlib to do a request over eachone link
        3.) open the file in write binary and write the chunk got in the request into the PDF file
        4.) finally if this steps fail print the name of the file that NOT FOUND 

        ''' 
        ctx = ssl.create_default_context()
        ctx.check_hostname = False
        ctx.verify_mode = ssl.CERT_NONE
        path = os.path.join(os.getcwd(), folder)
        if not os.path.exists(path):
            os.mkdir(path)
        for key,url in dictPDFs.items():
            response = urlopen(url, context=ctx)
            try:
                with open(os.path.join(path, key), 'wb+') as fd:
                    while True:
                        chunk = response.read(2000)
                        if not chunk:
                            break
                        fd.write(chunk)
            except:
                print(f'NOT FOUND: {key}')
                continue