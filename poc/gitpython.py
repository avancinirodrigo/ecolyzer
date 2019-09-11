from git import Repo

def show_tree_files(tree, spaces_count):
	spaces = ''
	spaces += ' ' * spaces_count
	for blob in tree.blobs:
		#print(blob.name)
		if blob.path == 'packages/base/lua/Cell.lua':
			print(spaces + '++', blob.name, blob.path, type(blob))
			data = blob.data_stream.read()
			print(data.decode('ascii'))

def show_tree_dirs(trees, spaces_count):
	spaces = ''
	spaces += ' ' * spaces_count
	if len(trees) > 0:
		for tree in trees:
			#print(spaces + '--', tree.name)
			show_tree_files(tree, spaces_count + 2)
			show_tree_dirs(tree.trees, spaces_count + 2)

path = 'repo/terrame'
repo = Repo(path)
git_dir = repo.git_dir

print(git_dir)

tree = repo.tree()
print(type(tree))
#for t in tree.trees:
#	print(t.name, type(t))
	#show_tree_dirs(t.trees, 2)
	#show_tree_files(t, 2)
	#print(t.__dict__)
	#print(' --', t.trees[0].name)
	#for b in t.blobs:
	#	print('   --', b.name, b.path)

for obj in tree:
    print(obj, type(obj.path), list(repo.iter_commits(paths=obj.path, max_count=1))[0])