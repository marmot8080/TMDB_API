import API_manager

if __name__ == '__main__':
    f = open("API_key.txt", 'r')
    api_key = f.readline()
    f.close()
    
    api_manager = API_manager.api_manager(api_key)