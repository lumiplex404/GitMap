#! /usr/bin/python3

try:
    import click
    import colorama as Palette
    import requests as https
    import os
except ModuleNotFoundError as error:
    print(f"\nModule \"{error.name}\" not found")
    exit()

Colors = Palette.Fore

WARN = Colors.YELLOW
INFO = Colors.BLUE
SUCCESS = Colors.GREEN
ERROR = Colors.RED

def colorPrint(text: str, type: Colors, end:str='\n'):
    print(type+text+"\n"+ERROR, end=end)


@click.command()
@click.argument('username', type = str)
@click.option('--details', '-d', is_flag=True, help="To see details about the user.")
@click.option('--displayPicture', '-dp', is_flag=True, help="To download the current profile picture of the user.")
@click.option('--repoAll', '-rA', is_flag=True, help="To see all the repositories of the user.")
@click.option('--repo', '-r', help="To see specific repository of the user.", type = str)
def fetch(username:str, repo:str, repoall:bool, details:bool, displaypicture: bool):

    # logo first
    print("\n", end="")

    colorPrint("[✔] All modules are present.", SUCCESS)
    colorPrint("[+] Starting GitMap...", SUCCESS)

    print("________________")
    print("| " + Colors.CYAN + "By CyberByte " + ERROR + "|")
    print("----------------")

    colorPrint(
'''
       ____________________________
       ||          _____         ||
       ||         < $ $ >        ||
       ||     ___  \ . /         ||
       ||        \ |   |         ||
       ||         / \  /\        ||
       ||        _\-----/_       ||
       ||________________________|| 
    ==================================
''', Colors.MAGENTA)

    # programme starts from here
    # check if none of the options were provided.
    if details or not details and not repo and not repoall and not displaypicture:    
        colorPrint(f"[!] Fetching data of ({username})...", WARN)
        try:
            res = https.get(f"https://api.github.com/users/{username}")

            match res.status_code:
                case 200:
                    usrDet = res.json()
                    colorPrint(
f'''GitHub profile link: {usrDet['html_url']}
Blog link: {usrDet['blog'] if usrDet['blog'] else None}

      * Account type: {usrDet['type']}
        Followers: {usrDet['followers']}
        Following: {usrDet['following']}
        Public Repositories: {usrDet['public_repos']}
        Public Gists: {usrDet['public_gists']}
      * Created at: {str(usrDet['created_at']).replace('T', " (yy/mm/dd) T ")}
      * Last updated at: {str(usrDet['updated_at']).replace('T', " (yy/mm/dd) T ")}

        Name: {usrDet['name']}
        username: {usrDet['login']}
      * Email: {usrDet['email']}
      * id: {usrDet['id']}
        node id: {usrDet['node_id']}
      * Location: {usrDet['location']}
        Bio: {usrDet['bio']}
      * Twitter: {usrDet['twitter_username'] if usrDet['twitter_username'] == None else f"https://twitter.com/{usrDet['twitter_username']}"}

        Company: {usrDet['company']}
        Site admin: {usrDet['site_admin']}
        Hireable: {usrDet['hireable']}
''', Colors.LIGHTWHITE_EX, end=""
                    )
                    colorPrint("[+] Data fetched successfully", SUCCESS)
                case 404:
                    colorPrint("[-] User not found.", ERROR)

        except https.exceptions.ConnectionError:
            colorPrint("[!] Please check your internet connection.", ERROR)

        except Exception as error:
            colorPrint(f"[-] {str(error)}", ERROR)

    if repoall:
        colorPrint(f"[!] Fetching repositories of ({username})...", WARN)
        try:
            response = https.get(f"https://api.github.com/users/{username}/repos")

            if response.status_code == 200:
                allReposData = response.json()
                colorPrint(f"[*] Total {len(allReposData)} public repositories found", INFO)

                for repoData in allReposData:
                    colorPrint(f"   →  {repoData['name']}", Colors.WHITE)
                colorPrint("[+] Repositories fetched successfully", SUCCESS)
            
            if response.status_code == 404:
                colorPrint("[-] No such user found!", ERROR)

        except https.exceptions.ConnectionError:
            colorPrint("[-] Please check your internet connection.", ERROR)

        except Exception as error:
            colorPrint(str(error), ERROR)
    else:
        if repo:
            colorPrint("[!] Fetching the repository...", WARN)

            try:
                response = https.get(f"https://api.github.com/repos/{username}/{repo}")

                if response.status_code == 200:
                    repoData = response.json()

                    colorPrint(
f'''[*] {username}/{repo} details:
GitHub repository link: {repoData['html_url']}

    Name: {repoData['name']}
    Path: {repoData['full_name']}
    Description: {repoData['description']}
    Forked: {repoData['fork']}
    Forked from: {repoData['parent']['html_url'] if repoData['fork'] else "None"}
    Allows Forking: {repoData['allow_forking']}
    Forks: {repoData['forks_count']}
    Language: {repoData['language'] if repoData['language'] else "No language detected"}

    Created at: {repoData['created_at'].replace('T', " (yy/mm/dd) T ")}
    Updated at: {repoData['updated_at'].replace('T', " (yy/mm/dd) T ")}
    Last pushed at: {repoData['pushed_at'].replace('T', " (yy/mm/dd) T ")}

    id: {repoData['id']}
    node id: {repoData['node_id']}
    SSH url: {repoData['ssh_url']}
    Git url: {repoData['git_url']}

    Topics: {repoData['topics']}
    Has issues: {repoData['has_issues']}
    Open issues: {repoData['open_issues']}
    Watchers: {repoData['watchers']}
    Subscribers: {repoData['subscribers_count']}
    Size: {repoData['size']}
    Is hosted: {repoData['has_pages']}
    Network count: {repoData['network_count']}
''', Colors.LIGHTWHITE_EX
                    )

            except https.exceptions.ConnectionError:
                colorPrint("[!] Please check your internet connection", ERROR)

            except Exception as error:
                print(response.status_code)
                colorPrint(f"[-] {str(error)}", ERROR)

    if displaypicture:

        colorPrint(f"[!] Fetching profile picture of ({username})...", WARN)

        try:
            usrRes = https.get(f"https://api.github.com/users/{username}")
            match usrRes.status_code:
                case 200:
                    picRes = https.get(f"{usrRes.json()['avatar_url']}")

                    with open(f"{usrRes.json()['login']}.png", "wb") as file:
                        file.write(picRes.content)

                    colorPrint("[+] Profile picture fetched successfully.", SUCCESS)
                    colorPrint(f"[*] Image Path: {os.getcwd()}/{usrRes.json()['login']}.png", WARN)
                case 404:
                    colorPrint("[-] User not found.", ERROR)

        except https.exceptions.ConnectionError:
            colorPrint("[-] Please check your internet connection.", ERROR)
            colorPrint("[-] Couldn't fetch profile picture of the user.", ERROR)
    
    colorPrint("[!] Programme closing...", WARN)
    return None

if __name__ == '__main__':
    fetch()
