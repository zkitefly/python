from flask import Flask, jsonify, redirect
from flask_caching import Cache
import httpx

app = Flask(__name__)
cache = Cache(app, config={'CACHE_TYPE': 'simple', 'CACHE_DEFAULT_TIMEOUT': 300})  # 300 seconds = 5 minutes

@app.route('/file/<path:file_name>')
@cache.cached(timeout=300)  # Cache the response for 5 minutes
def fetch_file(file_name):
    error_response = {
        "code": 404,
        "message": "File not found."
    }
    if "OptiFine_" not in file_name or not file_name.endswith(".jar"):
        return jsonify(error_response), 404

    url = f"https://optifine.net/adloadx?f={file_name}"
    response = httpx.get(url)
    text = response.text
    start = text.find("href='", text.find("<div class=\"downloadButton\">")) + len("href='")
    download_link = "https://optifine.net/" + text[start:text.find("'", start)]

    # Check if the download link is valid
    download_response = httpx.head(download_link)
    if download_response.status_code != 200 or 'Content-Disposition' not in download_response.headers:
        # Check the bmclapi version list
        version_list_response = httpx.get("https://bmclapi2.bangbang93.com/optifine/versionList")
        if version_list_response.status_code != 200:
            return jsonify(error_response), 404
        version_list = version_list_response.json()
        for version_info in version_list:
            if version_info['filename'] == file_name:
                mc_version = version_info['mcversion']
                patch = version_info['patch']
                optifine_type = version_info['type']
                redirect_url = f"https://bmclapi2.bangbang93.com/optifine/{mc_version}/{optifine_type}/{patch}"
                bmclapi_redirect_response = redirect(redirect_url)
                bmclapi_redirect_response.headers['Cache-Control'] = 'max-age=0, s-maxage=300' # Add the Cache-Control header, https://vercel.com/docs/edge-network/headers#recommended-settings
                return bmclapi_redirect_response
        # If the file name is not found in the version list
        return jsonify(error_response), 404

    # If the download link is valid, return a redirect response
    redirect_response = redirect(download_link)
    redirect_response.headers['Cache-Control'] = 'max-age=0, s-maxage=300' # Add the Cache-Control header, https://vercel.com/docs/edge-network/headers#recommended-settings
    return redirect_response

if __name__ == "__main__":
    app.run()
