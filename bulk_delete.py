import requests, json, getpass

class Vars():
	source_url=""
	admin_username=""
	admin_password=""
	headers={'X-Atlassian-Token': 'nocheck'}
	api_session=None

def get_creds():
	Vars.source_url = input("Enter URL of Bitbucket instance:\n")
	Vars.admin_username = input("Enter admin username:\n")
	Vars.admin_password = getpass.getpass("Enter Admin password:\n")
	Vars.api_session = requests.Session()
	Vars.api_session.auth = (Vars.admin_username, Vars.admin_password)

def read_list_of_users_to_del():
	with open("del_users.json", "r") as infile:
		user_dictionary = json.load(infile)
		user_list = user_dictionary['name']
	return user_list

def delete_users(user):
	params = {'name': user}
	try:
		r = Vars.api_session.delete(Vars.source_url + '/rest/api/1.0/admin/users', params=params, headers=Vars.headers)
	except requests.exceptions.SSLError:
		r = Vars.api_session.delete(Vars.source_url + '/rest/api/1.0/admin/users', params=params, headers=Vars.headers, verify=False)

def main():
	get_creds()
	user_list = read_list_of_users_to_del()
	for user in user_list:
		delete_users(user)

if __name__ == "__main__":
	main()