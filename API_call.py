import API_manager
import json
import datetime
import time
import os

if __name__ == '__main__':
    f = open("API_key.txt", 'r')
    api_key = f.readline()
    f.close()
    
    api_manager = API_manager.api_manager(api_key)

    state_file_name = 'state.json'
    json_file = open(state_file_name, 'r')
    state = json.load(json_file)

    recent_date = datetime.datetime.strptime(state['recent_date'], "%Y-%m-%d").date()
    today = datetime.datetime.today().date()

    while recent_date + datetime.timedelta(14) < today:
        print(recent_date.strftime("%Y-%m-%d") + "~" + (recent_date + datetime.timedelta(13)).strftime("%Y-%m-%d"))
        json_file = open(state_file_name, 'r')
        state = json.load(json_file)
        
        total_page = api_manager.get_total_pages(recent_date.strftime("%Y-%m-%d"), (recent_date + datetime.timedelta(13)).strftime("%Y-%m-%d"))

        for page in range(state['page'], total_page + 1):
            print('(' + str(page) + '/' + str(total_page) + ')')
            movie_ids = api_manager.get_movie_ids(recent_date.strftime("%Y-%m-%d"), (recent_date + datetime.timedelta(13)).strftime("%Y-%m-%d"), page)
            time.sleep(0.2)

            for id in movie_ids:
                details = api_manager.get_movie_detail(id)
                if not details == None:
                    api_manager.wirte_movie_detail(details)
                    time.sleep(0.2)
                
            state['page'] = page + 1

            with open(state_file_name, 'w', encoding='utf-8') as temp_file:
                json.dump(state, temp_file, indent='\t')

        recent_date += datetime.timedelta(14)
        state['recent_date'] = recent_date.strftime("%Y-%m-%d")
        state['page'] = 1

        with open(state_file_name, 'w', encoding='utf-8') as json_file:
            json.dump(state, json_file, indent='\t')

    del api_manager