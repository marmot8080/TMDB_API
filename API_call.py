import API_manager
import json
import datetime
import time

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
        json_file = open(state_file_name, 'w', encoding='utf-8')
        
        movie_ids = api_manager.get_movie_ids(recent_date.strftime("%Y-%m-%d"), (recent_date + datetime.timedelta(14)).strftime("%Y-%m-%d"))
        time.sleep(0.2)

        for i in range(state['page'] - 1, len(movie_ids)):
            for id in movie_ids[i]:
                details = api_manager.get_movie_detail(id)
                api_manager.wirte_movie_detail(details)
                time.sleep(0.2)
            
            state['page'] = i + 1
            json.dump(state, json_file, indent='\t')

        state['recent_date'] = recent_date.strftime("%Y-%m-%d")
        json.dump(state, json_file, indent='\t')
        recent_date += datetime.timedelta(14)

    del api_manager