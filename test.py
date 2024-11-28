def parse_url(client_id, scope, response_type, redirect_uri):
    "https://accounts.google.com/o/oauth2/v2/auth/oauthchooseaccount?client_id=901368089247-rpdkiisqf3i4rfjim66cd6s6106dibje.apps.googleusercontent.com&scope=openid email profile&response_type=id_token&gsiwebsdk=gis_attributes&redirect_uri=https%3A%2F%2Fidentity.deliveroo.com&response_mode=form_post&origin=https%3A%2F%2Fidentity.deliveroo.com&display=popup&prompt=select_account&gis_params=Ch5odHRwczovL2lkZW50aXR5LmRlbGl2ZXJvby5jb20SHmh0dHBzOi8vaWRlbnRpdHkuZGVsaXZlcm9vLmNvbRgHKhZQRXZhZnh4Yk5jcmhYQlBrVUpZZFlnMkg5MDEzNjgwODkyNDctcnBka2lpc3FmM2k0cmZqaW02NmNkNnM2MTA2ZGliamUuYXBwcy5nb29nbGV1c2VyY29udGVudC5jb204AUJANWUxNzEwM2E0NmUxMDRkZGFmNWIyMWMwOTQ0ZmY1YmE3NjI4ZmViODE3N2NlOTdlOTZjMjI3YjQ0NzFmMGE0Yw&service=lso&o2v=1&ddm=1&flowName=GeneralOAuthFlow"
    return f"https://accounts.google.com/o/oauth2/v2/auth/oauthchooseaccount?client_id={client_id}&scope={scope}&response_type={response_type}&gsiwebsdk=gis_attributes&redirect_uri={redirect_uri}&response_mode=form_post&origin={redirect_uri}&display=popup&prompt=select_account&gis_params=Ch5odHRwczovL2lkZW50aXR5LmRlbGl2ZXJvby5jb20SHmh0dHBzOi8vaWRlbnRpdHkuZGVsaXZlcm9vLmNvbRgHKhZQRXZhZnh4Yk5jcmhYQlBrVUpZZFlnMkg5MDEzNjgwODkyNDctcnBka2lpc3FmM2k0cmZqaW02NmNkNnM2MTA2ZGliamUuYXBwcy5nb29nbGV1c2VyY29udGVudC5jb204AUJANWUxNzEwM2E0NmUxMDRkZGFmNWIyMWMwOTQ0ZmY1YmE3NjI4ZmViODE3N2NlOTdlOTZjMjI3YjQ0NzFmMGE0Yw&service=lso&o2v=1&ddm=1&flowName=GeneralOAuthFlow"

def extract_parameters(url):
    params = {'client_id': '',
            'scope': '',
            'response_type': '',
            'redirect_uri': ''}
    url = url.split('?')[1]
    url = url.split('&')
    for i in url:
        key = i.split('=')[0]
        if key in params:
            params[key] = i.split('=')[1]
    return params
    


#print(parse_url("901368089247-rpdkiisqf3i4rfjim66cd6s6106dibje.apps.googleusercontent.com", "openid email profile", "id_token", "https://identity.deliveroo.com"))

#print(extract_parameters("https://accounts.google.com/o/oauth2/v2/auth/oauthchooseaccount?client_id=901368089247-rpdkiisqf3i4rfjim66cd6s6106dibje.apps.googleusercontent.com&scope=openid email profile&response_type=id_token&gsiwebsdk=gis_attributes&redirect_uri=https%3A%2F%2Fidentity.deliveroo.com&response_mode=form_post&origin=https%3A%2F%2Fidentity.deliveroo.com&display=popup&prompt=select_account&gis_params=Ch5odHRwczovL2lkZW50aXR5LmRlbGl2ZXJvby5jb20SHmh0dHBzOi8vaWRlbnRpdHkuZGVsaXZlcm9vLmNvbRgHKhZQRXZhZnh4Yk5jcmhYQlBrVUpZZFlnMkg5MDEzNjgwODkyNDctcnBka2lpc3FmM2k0cmZqaW02NmNkNnM2MTA2ZGliamUuYXBwcy5nb29nbGV1c2VyY29udGVudC5jb204AUJANWUxNzEwM2E0NmUxMDRkZGFmNWIyMWMwOTQ0ZmY1YmE3NjI4ZmViODE3N2NlOTdlOTZjMjI3YjQ0NzFmMGE0Yw&service=lso&o2v=1&ddm=1&flowName=GeneralOAut"))

params = extract_parameters("https://accounts.google.com/o/oauth2/v2/auth/oauthchooseaccount?client_id=901368089247-rpdkiisqf3i4rfjim66cd6s6106dibje.apps.googleusercontent.com&scope=openid email profile&response_type=id_token&gsiwebsdk=gis_attributes&redirect_uri=https%3A%2F%2Fidentity.deliveroo.com&response_mode=form_post&origin=https%3A%2F%2Fidentity.deliveroo.com&display=popup&prompt=select_account&gis_params=Ch5odHRwczovL2lkZW50aXR5LmRlbGl2ZXJvby5jb20SHmh0dHBzOi8vaWRlbnRpdHkuZGVsaXZlcm9vLmNvbRgHKhZQRXZhZnh4Yk5jcmhYQlBrVUpZZFlnMkg5MDEzNjgwODkyNDctcnBka2lpc3FmM2k0cmZqaW02NmNkNnM2MTA2ZGliamUuYXBwcy5nb29nbGV1c2VyY29udGVudC5jb204AUJANWUxNzEwM2E0NmUxMDRkZGFmNWIyMWMwOTQ0ZmY1YmE3NjI4ZmViODE3N2NlOTdlOTZjMjI3YjQ0NzFmMGE0Yw&service=lso&o2v=1&ddm=1&flowName=GeneralOAut")
print(parse_url(params['client_id'], params['scope'], params['response_type'], params['redirect_uri']))