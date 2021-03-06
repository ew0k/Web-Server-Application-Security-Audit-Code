'''
file: HTTP_Parser.py
language: python3
author: Jacob Brown jmb7438@rit.edu
description: HTTP parser that verifies the syntax of a HTTP request
'''

import sys
import Response_Codes


def print_usage():
    """Print the usage message of this script
    
    Parameters
    ----------
    None

    Returns
    -------
    Nothing
    """
    print("Usage: HTTP_Parser.py path_to_http_file")


def gather_input():
    """Gather input from the command line and exit if input is incorrect
    
    Parameters
    ----------
    None

    Returns
    -------
    string
        File with HTTP request opened for reading in binary mode 
    """
    if len(sys.argv) != 2:
        print_usage()
        exit(1)
    else:
        return open(sys.argv[1], 'rb').readlines()


def verify_method(method):
    """Verify that the method used is allowed by a predetermined list.
    Return a 400 code and exit if it is not.
    
    Parameters
    ----------
    method : string
        Method to verify
    
    Returns
    -------
    Nothing
    """ 
    allowed_methods = [
        "GET",
        "POST",
        "PUT",
        "DELETE",
        "CONNECT",
        "HEAD"
    ]

    if method.upper() not in allowed_methods:
        Response_Codes.respond_with_400()


def verify_request_uri(request_uri):
    """Verify that the request URI is valid. Return a 400 code and exit if it is not.
    Note: This function was not needed for this assignment.
          It will be implemented at a later time when it is needed
    
    Parameters
    ----------
    request_uri : string
        Request URI to verify
    
    Returns
    -------
    Nothing
    """
    pass


def verify_http_version(http_version):
    """Verify the HTTP 1.1 is used. Return a 400 code and exit if it is not.
    
    Parameters
    ----------
    http_version : string
        HTTP version string to verify
    
    Returns
    -------
    Nothing
    """
    if http_version != "HTTP/1.1":
        Response_Codes.respond_with_400()


def verify_request_line(request_line):
    """Verify the syntax of the request line. The syntax should follow the following production rule:
    Request-Line = Method SP Request-Target SP HTTP-Version CRLF
    Return a 400 code and exit if it is not valid.
    
    Parameters
    ----------
    request_line : string
        request line to verify
    
    Returns
    -------
    Nothing
    """
    if request_line.count(" ") != 2:
        Response_Codes.respond_with_400()
    
    split_request_line = request_line.split(" ")
    method = split_request_line[0]
    verify_method(method)

    request_uri = split_request_line[1]
    verify_request_uri(request_uri)

    http_version = split_request_line[2]
    verify_http_version(http_version)


def verify_header(header):
    """Verify that the syntax of an individual header is correct
    
    Parameters
    ----------
    header : string
        Individual header to validate
    
    Returns
    -------
    int
        1 if "Host" header is found, 0 otherwise
    """
    if header.count(':') != 1:
        Response_Codes.respond_with_400()
    header = header.replace(" ", "")
    key = header.split(":")[0]

    if key.lower() == "host":
        return 1
    return 0

def verify_headers(headers):
    """Verify that all headers are syntaxually correct and that the "Host" header is included
    
    Parameters
    ----------
    headers : list
        List of headers to verify
    
    Returns
    -------
    Nothing
    """
    count = 0
    for header in headers:
        count += verify_header(header)
    if count != 1:
        Response_Codes.respond_with_400()


def parse_request(request):
    """Parse a HTTP request and check for syntax. If syntax is correct, respond with a 400 HTTP code.
    Otherwise, respond with a 200 HTTP code.
    
    Parameters
    ----------
    request : list
        HTTP request read from a file in the following way: open(file_name, 'rb').readlines()
    
    Returns
    -------
    Nothing
    """
    request_str = ""
    for line in request:
        request_str += str(line)[2:-1]

    if request_str.count("\\r\\n\\r\\n") != 1:
        Response_Codes.respond_with_400()
    
    request_line_and_headers = request_str.split("\\r\\n\\r\\n")[0]

    request_line = request_line_and_headers.split("\\r\\n")[0]
    verify_request_line(request_line)

    request_headers = request_line_and_headers.split("\\r\\n")[1:]
    verify_headers(request_headers)

    Response_Codes.respond_with_200()
    

def main():
    try:
        http_file = gather_input()
        parse_request(http_file)
    except Exception:
        Response_Codes.respond_with_500()

    
main()