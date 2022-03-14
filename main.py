from git import Repo
import datetime
from progress.bar import Bar
import operator
import sys


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

def getCommitsPerModule(commits_list, dir_to_search):
	commits_per_module = {}

	# parse the dir path and get module names and the number of commits per module
	for directory in commits_list:
		splits = directory.split('/')
		if splits[0] == dir_to_search and len(splits[1].split('.')) == 1:
			if splits[1] in commits_per_module:
				commits_per_module[splits[1]] += 1
			else:
				commits_per_module[splits[1]] = 1

	return commits_per_module

def getChurns(git_repo, sha_list, dir_to_search):
	churn_per_module = {}
	bar = Bar('Getting chur per modules', max=(len(sha_list)-1))

	# find the diff between two sha and count the number of changes per module
	for i in range(len(sha_list)-1):
		diffInfo = git_repo.diff('{}..{}'.format(sha_list[i],sha_list[i+1])).split('\n')
		for j in range(len(diffInfo)):
			splits = diffInfo[j].split(' ')
			module = ''
			if splits[0] == 'diff':
				dir_path = splits[2].split('/')
				if dir_path[1] == dir_to_search:
					module = dir_path[2]
					if len(module.split('.')) == 2:
						continue 
					if module not in churn_per_module:
						churn_per_module[module] = 0
					k = j + 1
					while True and k < len(diffInfo):
						splits = diffInfo[k].split(' ')
						if splits[0] == 'diff':
							j = k
							break
						if splits[0] == '+' or splits[0] == '-':
							churn_per_module[module] += 1
						k += 1
		bar.next()
	bar.finish()
	return churn_per_module


def main():
	try:
		working_dir = sys.argv[1]
		dir_to_search = sys.argv[2]
	except Exception as e:
		print('Missing an Argument!!')
		return

	months = 6
	days = 30

	repo = Repo(working_dir)
	git_repo = repo.git
	current_date = datetime.date.today()
	since = current_date - datetime.timedelta(months * days)
	
	print('Getting Commited directories')
	commit_dirs = getDirs(git_repo, since)
	
	print('Getting SHAs of each Commits')
	sha_list = getSHAs(git_repo, since)
	
	print('Getting Commit per modules')
	commits_per_module = getCommitsPerModule(commit_dirs, dir_to_search)

	churn_per_module = getChurns(git_repo, sha_list, dir_to_search)
	
	# sort the commits_per_module by number of commits and get top 12
	sorted_module_commit = dict(sorted(commits_per_module.items(), key=operator.itemgetter(1),reverse=True)[:12])

	print('Top modules with highest number of commits:')
	for module in sorted_module_commit.keys():
		print(' ' * 2 + module)

	print()

	# sort the churn_per_module by number of commits and get top 12	
	sorted_module_churn = dict(sorted(churn_per_module.items(), key=operator.itemgetter(1),reverse=True)[:12])

	print('Top modules with highest number of churns:')
	for module in sorted_module_churn.keys():
		print(' ' * 2 + module)


if __name__ == '__main__':
	main()
