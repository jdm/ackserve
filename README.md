ackserve
========

This is a quick'n'dirty implementation of an interface like Mozilla's MXR (http://mxr.mozilla.org),
but replacing static code indexes with a local Python-based HTTP server that shells out to the `ack`
utility. The main use case is to allow opening the results of ack searches in new tabs and retaining
search history more efficiently, but ackserve also displays syntax-highlighted files, along with
directory listings, and the search results are clickable links to lines of matching files.

To use ackserve, first ensure the `ack` binary is in your PATH. Note that on Debian-based distributions
the `ack` tool goes by `ack-grep` and is not currently supported.

git clone https://github.com/jdm/ackserve.git
cd ackserve
python -m CGIHTTPServer
firefox http://localhost:8000/?path=/absolute/path/to/project/root
