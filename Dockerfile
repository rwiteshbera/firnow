FROM nginx:latest

EXPOSE 80

WORKDIR /home/nginx

RUN mkdir -p docs && mkdir -p nvm && mkdir -p duckdns

COPY ./nginx/nginx.conf /etc/nginx/nginx.conf
COPY ./env.list .

SHELL ["/bin/bash", "-ec"]

RUN export $(grep -v '^#' env.list | xargs) \
    && export NVM_DIR=/home/nginx/nvm \
    && export PATH="$PATH:$NVM_DIR/versions/node/*/bin/node" \
    && curl -o- https://raw.githubusercontent.com/nvm-sh/nvm/v0.39.7/install.sh | bash \
    && source ~/.bashrc \
    && nvm install 20 \
    && npm i @redocly/cli@latest \
    && echo "$REDOCLYTOKEN" | node node_modules/.bin/redocly login \
    && echo "echo url=\"https://www.duckdns.org/update?domains=firnow&token=$DUCKDNSTOKEN&ip=\" | curl -k -o /home/nginx/duckdns/duck.log -K -" > duckdns/duck.sh \
    && chmod 700 duckdns/duck.sh \
    && ./duckdns/duck.sh

# COPY ./patched/* /home/nginx/.nvm/versions/node/v20.13.1/lib/node_modules/@redocly/cli/lib/commands/preview-docs/preview-server/

COPY ./patched/* node_modules/@redocly/cli/lib/commands/preview-docs/preview-server/

# RUN nohup redocly preview-docs --port 8000 &
# CMD ["/home/nginx/nvm/versions/node/*/bin/node", "node_modules/.bin/redocly", "preview-docs", "--port", "8000", "&", "&&", "nginx", "-g", "daemon off;"]
CMD ["nginx", "-g", "daemon off;"]