## GIT workflow ##

The following links give basic guidelines which we draw from to develop
our GIT workflow.

  * [http://nvie.com/posts/a-successful-git-branching-model/]()
  * [https://geekbacon.com/2015/07/30/git-workflow-branching-strategy-and-release-management/]()
  * [http://thesp0nge.tumblr.com/post/10123266526/choosing-a-good-version-numbering-policy]()


### Branching Overview ###
![git-model@2x.png](https://bitbucket.org/repo/jBdny9/images/2870060732-git-model@2x.png)

#### Branch naming ####

We will use multiple GIT branches to manage development

  * master
  * release
  * develop
  * bugfix-\*
  * personal and feature branchces


#### Branch rules ####

**master** branch will be the one containing the code that is always production ready in a given moment.

Branches cannot be created from **master** except for bugfixes. Bugfixes branches will be named 'bugfix-id' where ID will be an incrementing number starting with 1.

The **develop** branch was originally created from **master**

The **develop** branch will be the primary development branch.

Code in **develop** should pass all regression tests and not generate any errors under normal use.

Many other branches can be created from **develop** to create and test new features.

Tags will be used in the **master** branch to denote release versions.


#### Tags ####

Our version system will have the basic structure as follows:

    <major version>.<minor version>.<bugfix version>

Our *major version* will be slow to change and will denote a major release manually created.

The *minor version* will be as follows:

  * Public releases will always have an even number.
  * Private and semi-public release candidates will have odd numbers.


#### Tag Workflow Example: ####

  * The initial public 1.0 release. *1.0.0*
  * A new bug was found and fixed. *1.0.1*, *1.0.2*
  * A new set of features for a beta release are being tested. *1.1.0*
  * Our beta release candidate is ready for production. We increment the version. *1.2.0*
  * More bugs are found. New release is *1.2.1*
  * Continued bug fixes over time. Releases *1.2.2*, *1.2.3*, *1.2.4*



#### Branch Workflow Example: ####

##### Getting started. Adding a new feature. #####

  * *git checkout -b newfeature-branch develop*
  * Create the feature
  * *git add .*
  * *git commit -m 'New feature'*


##### Merging new feature. #####

  * *git checkout develop*
  * *git pull origin develop*
  * *git merge --no-ff newfeature-branch*

    *--no-ff* does create a empty commit object but the trade-off is worth it. We don't fast-forward because we want to keep historical information about the feature branch and all its commits that create the feature. This also makes it easier if you need to revert a whole feature.

  * *git branch -d newfeature-branch*
  * *git push origin develop*


##### Creating a new release #####

  * *git checkout -b release-1.2 develop*
  * *git commit -am "Release 1.2 version bump."*


##### Merging release into the master branch #####

  * *git checkout master*
  * *git merge --no-ff release-1.2*
  * *git tag -a 1.2 -m "Release version 1.2"*

    When merging to **master** we always tag.

  * *git push --tags*

    Annotated tags aren't tied to a specific branch, but are objects of their own with metadata. It contains the commit, tagger, date, author, etc. Lightweight tags are basically pointers to a commit hash.

  * *git checkout develop*
  * *git merge --no-ff release-1.2*

    This may introduce a merge conflict due to the version changes which we can fix and commit again.

  * *git branch -d release-1.2*


##### Create new bugfix branches #####

  * *git checkout -b bugfix-1.2.1 master*
  * *git commit -am "Version bump to 1.2.1"*
  * Fix the bug
  * *git commit -m "Production bugfix. JIRA issue RX-12"*


##### Merge bugfix branch #####

  * *git checkout master*
  * *git merge --no-ff bugfix-1.2.1"*
  * *git tag -a 1.2.1 -m "Bugfix version 1.2.1"

    Again we always tag on **master** branch.

  * *git push --tags*
  * *git checkout develop*
  * *git merge --no-ff bugfix-1.2.1*
  * *git branch -d bugfix-1.2.1*
