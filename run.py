#!/usr/bin/env python3

import webapp

def main():

    print("Running File Encryptor web app!")
    webapp.app.run(host='0.0.0.0', port=12345, threaded=True, debug=True)

if __name__ == "__main__":
    main()