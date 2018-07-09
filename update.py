import urllib.request
import os
import time
import json
import datetime
import urllib

# do not forget to setup the cron-job in order to make this process automated.
# Required data from Weather Underground

# you can define variables here or via URL, make sure to comment out or delete hardcoded variables to get them from URL
#	start of hardcoded variables
# API key https:#www.wunderground.com/weather/api/
wuAPI = "03a748ed55456f18" # change contents, keep quotes
wuID = "KCADANVI59"

# Data needed from PWS weather
pwsID = "KCADANVI59" # change contents, keep quotes
# pwsID = filter_var("FexampleER", FILTER_SANITIZE_STRING) # Example of sanitized variable, worth trying if you run into errors
psw = "K04ZLQlDhvt7" # seems to dislike commas, try simplier password in case you get ID/pass error (periods "." are ok)

#set the time zone here
os.environ['TZ'] = 'America/Los_Angeles'
time.tzset()
# 	End of hardcoded variables

# get missing data from URL (if available)
# if(!isset(wuAPI))
# 	wuAPI = filter_input(INPUT_GET,"wuAPI",FILTER_SANITIZE_STRING)
# if(!isset(wuID))
# 	wuID = filter_input(INPUT_GET,"wuID",FILTER_SANITIZE_STRING)
# if(!isset(pwsID))
# 	pwsID = filter_input(INPUT_GET,"pwsID",FILTER_SANITIZE_STRING)
# if(!isset(psw))
# 	psw = filter_input(INPUT_GET,"psw",FILTER_SANITIZE_STRING)

# start of code

if psw:
	
	url = 'http://api.wunderground.com/api/' + wuAPI + '/conditions/q/pws:' + wuID + '.json'
	# print (url)
	webUrl = urllib.request.urlopen(url)
	wuData = webUrl.read()
	# print (wuData)
	data = json.loads(wuData)
	
	utctime = datetime.datetime.utcnow()
	#print(utctime)

	if data['current_observation']:
		print (data['current_observation']['observation_epoch'])

		# date = datetime('@' + data['current_observation']['observation_epoch'])
		# print date.strftime('%Y-%m-%d %H:%M:%S', time.gmtime(data['current_observation']['observation_epoch']))
		
		delta = time.time() - int(data['current_observation']['observation_epoch'])
		print('time delta is ' + str(delta))
		
		if(delta > 2000): # to get rid of old data spikes
			
			echo('The data from ' + delta + ' seconds ago was too old for trasfer, will retry on next attempt')
			
		else:
			dict_name_value_pair = {
				"ID" : pwsID,
				"PASSWORD" : psw,
				"softwaretype" : "ebviaphpV0.3",
				"action" : "updateraw",
				"dateutc" : str(utctime)[: 19],
			}
			if float(data['current_observation']['wind_degrees']) >= 0: 
				dict_name_value_pair["winddir"] = data['current_observation']['wind_degrees'] 
			if float(data['current_observation']['wind_mph']) >= 0:
				dict_name_value_pair["windspeedmph"] = data['current_observation']['wind_mph'] 
			if float(data['current_observation']['wind_gust_mph']) >= 0:
				dict_name_value_pair["windgustmph"] =  data['current_observation']['wind_gust_mph']
			# I would be impressed if anyone recorded temperatures close to absolute zero.
			if float(data['current_observation']['temp_f']) > -459:
				dict_name_value_pair["tempf"] = data['current_observation']['temp_f'] 
			if float(data['current_observation']['precip_1hr_in']) >= 0:
				dict_name_value_pair["rainin"] = data['current_observation']['precip_1hr_in']
			if float(data['current_observation']['precip_today_in']) >= 0:
				dict_name_value_pair["dailyrainin"] = data['current_observation']['precip_today_in']
			if float(data['current_observation']['pressure_in']) >= 0:
				dict_name_value_pair["baromin"] = data['current_observation']['pressure_in']
			if float(data['current_observation']['dewpoint_f']) > -100:
				dict_name_value_pair["dewptf"] = data['current_observation']['dewpoint_f']
			if (data['current_observation']['relative_humidity'])[:1] != '-':
				dict_name_value_pair["humidity"] = data['current_observation']['relative_humidity'][: -1]
			print (dict_name_value_pair)
			url = 'http://www.pwsweather.com/pwsupdate/pwsupdate.php?' + urllib.parse.urlencode(dict_name_value_pair) 
		
			print (url)
			webUrl = urllib.request.urlopen(url)
			pwsdata = webUrl.read()

			print (pwsdata)
			
# 			results = pwsdata.split('\n')

# 			if (results[6]) = 'ERROR: Not a vailid Station ID':
# 				echo ('We got an error from PWS weather: Your PWS weather ID (pwsID) appears to be invalid')
# 			else:
# 				if (results[6]) = 'ERROR: Not a vailid Station ID/Password':
# 					echo ('We got an error from PWS weather: Your PWS account password (psw) appears to be invalid')
# 				else:
# 					if (results[6]) = 'Data Logged and posted in METAR mirror.':
# 						echo('The latest data from ' + delta + ' seconds ago was transfered to PWS weather station ' + pwsID)
# 		echo pwsdata

		
# 	else:
# 			#http_response_code(400) # bad request 
# 			# we got an error
# 			if data['response']['error']):
# 				echo ('We got an error from Weather Underground: ')

# 			if (data['response']['error']['type']) = "keynotfound":
# 					echo('Your Weather Underground API key (wuAPI) appears to be invalid')
# 			if (data['response']['error']['type']) = "Station:OFFLINE":
# 					echo('Your Weather Underground Station ID (wuID) appears to be invalid')
# 			else:
# 					echo('This appears to be a temporary error, please try again later')
# 					echo('Exact Error type: " . data['response']['error']['type']')
# 					echo('Which means: " . data['response']['error']['description']')
	
# else:
# 	echo ('Not enough URL or Hardcoded parameters')
# }

