from git import Repo
import datetime

def getDirs(git_repo, since):
	return git_repo.log('--since={}'.format(since), '--pretty=tformat:', '--name-only').split('\n')


def getSHAs(git_repo, since):
	commits = git_repo.log('--since={}'.format(since)).split('\n')

	sha_list = []

	for line in commits:
		split_line = line.split(' ') 
		if split_line[0] == 'commit':
			sha_list.append(split_line[1])

	return sha_list


def main():
	working_dir = 'C:\\Users\\suzan\\Documents\\git analysis\\nova'
	months = 6
	days = 30

	repo = Repo(working_dir)
	git_repo = repo.git
	current_date = datetime.date.today()
	since = current_date - datetime.timedelta(months * days)
	
	commit_dirs = getDirs(git_repo, since)
	sha_list = getSHAs(git_repo, since)
	
	modules = []
	commits_per_module = {}
	for directory in commit_dirs:
		splits = directory.split('/')
		if splits[0] == 'nova' and len(splits[1].split('.')) == 1:
			modules.append(splits[1])

			if splits[1] in commits_per_module:
				commits_per_module[splits[1]] += 1
			else:
				commits_per_module[splits[1]] = 1

	print(commits_per_module)
	# print('{}...{}'.format(sha_list[1],sha_list[3]))
	# diffs = git_repo.diff('{}..{}'.format(sha_list[1],sha_list[3]))
	# print(diffs)

if __name__ == '__main__':
	main()
