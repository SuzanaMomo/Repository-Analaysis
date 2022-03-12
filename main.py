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

def getCommitsPerModule(commits_list):
	# modules = []
	commits_per_module = {}
	for directory in commits_list:
		splits = directory.split('/')
		if splits[0] == 'nova' and len(splits[1].split('.')) == 1:
			# modules.append(splits[1])
			if splits[1] in commits_per_module:
				commits_per_module[splits[1]] += 1
			else:
				commits_per_module[splits[1]] = 1

	return commits_per_module

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
	
	commits_per_module = getCommitsPerModule(commit_dirs)


	churn_per_module = {}

	for i in range(len(sha_list)-1):
		diffInfo = git_repo.diff('{}..{}'.format(sha_list[i],sha_list[i+1])).split('\n')
		# print(i)
		for j in range(len(diffInfo)):
			splits = diffInfo[j].split(' ')
			module = ''
			if splits[0] == 'diff':
				# print(j)
				dir_path = splits[2].split('/')
				if dir_path[1] == 'nova':
					module = dir_path[2]
					if len(module.split('.')) == 2:
						continue 
					if module not in churn_per_module:
						churn_per_module[module] = 0
					k = j + 1
					while True and k < len(diffInfo):
						splits = diffInfo[k].split(' ')		
						# print(splits)	
						if splits[0] == 'diff':
							j = k
							break
						if splits[0] == '+' or splits[0] == '-':
							churn_per_module[module] += 1
						k += 1
					# # print(j)
		# break
	# print(len(sha_list))
	print(churn_per_module)

if __name__ == '__main__':
	main()
