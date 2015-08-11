from flask import Flask
from flask_slack import Slack
from rdoclient import RandomOrgClient as rorgcli
import os

app = Flask(__name__)
slack = Slack(app)
app.add_url_rule('/', view_func=slack.dispatch)

slacktoken = os.getenv('SLACKTOKEN')
randokey = os.getenv('RANDOMORG_KEY')
team = os.getenv('SLACKTEAM')

def random_client():
    rnd = rorgcli(randokey)
    return rnd

rnd = random_client()

def strategy():
    with open('oblique.txt', 'r') as ost:
        strats = ost.readlines()
        length = len(strats)
    idx = rnd.generate_integers(1, 0, length)
    strat = strats[idx[0]].strip()
    return strat

def i_ching():
    with open('iching-title.txt', 'r') as i:
        chis = i.readlines()
    idx = rnd.generate_integers(1,0,63)
    hexagram = chis[idx[0]].strip()
    hexagram_no = [idx[0]] + 1
    url = 'http://www.akirarabelais.com/i/i.html#%s' % hexagram_no
    return {'hexagram': hexagram, 'url': url}


@slack.command('oblique', token=slacktoken,
               team_id=team, methods=['POST'])
def oblique(**kwargs):
    strat = strategy()
    iching = i_ching()
    url = iching['url']
    hexagram = iching['hexagram']
    message = '%s\n <%s|%s>' % (strat, url, hexagram)
    return slack.response(message)

@app.route('/strategy')
def index():
    strat = strategy() + '\n'
    return strat


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)