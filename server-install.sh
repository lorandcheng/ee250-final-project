#THIS IS NOT ACTUALLY MEANT FOR EXECUTION

sudo apt-get update
sudo apt-get install git -y
sudo apt-get -y install python3-pip
sudo pip3 install flask python-dotenv

ssh-keygen -t ed25519 -C "lfcheng@usc.edu"
cd ~/.ssh
eval "$(ssh-agent -s)"
ssh-add ~/.ssh/id_ed25519
cat ~/.ssh/id_ed25519.pub
# add this ssh public key to github
PAUSE
cd ~
git clone git@github.com:lorandcheng/ee250-final-project.git
cd ee250-final-project
