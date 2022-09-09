import requests
import json

def get_page_release(url,page):
    return requests.get(url,
                            params={'per_page' : '100','page' : page},
                            headers={'Accept': 'application/vnd.github.v3+json'})


def spring_releases():
    all_releases = get_github_releases("https://api.github.com/repos/spring-projects/spring-boot/releases")
    write_results(all_releases,"data/spring_boot_releases.json")


def get_github_releases(url):
    all_releases = []
    page = 1
    while page != 0:
        response = get_page_release(url, page)
        if "next" in response.links:
            page = page + 1
        else:
            page = 0
        for item in response.json():
            #        release_details = item['name'] + "," +  item['published_at'] + "," + item['html_url']
            release_details = {"version": item['name'], "date": item['published_at'], "url": item['html_url']}
            all_releases.append(release_details)
    return all_releases


def write_results(all_releases,results_file):
    f = open(results_file, "w")
    f.write(json.dumps(all_releases))
    f.close()


def k8s_releases():
    all_releases = get_github_releases("https://api.github.com/repos/kubernetes/kubernetes/releases")
    write_results(all_releases, "data/kubernetes_releases.json")


spring_releases()
k8s_releases()
