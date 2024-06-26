"use strict";
var __awaiter = (this && this.__awaiter) || function (thisArg, _arguments, P, generator) {
    function adopt(value) { return value instanceof P ? value : new P(function (resolve) { resolve(value); }); }
    return new (P || (P = Promise))(function (resolve, reject) {
        function fulfilled(value) { try { step(generator.next(value)); } catch (e) { reject(e); } }
        function rejected(value) { try { step(generator["throw"](value)); } catch (e) { reject(e); } }
        function step(result) { result.done ? resolve(result.value) : adopt(result.value).then(fulfilled, rejected); }
        step((generator = generator.apply(thisArg, _arguments || [])).next());
    });
};
Object.defineProperty(exports, "__esModule", { value: true });
const handlebars_1 = require("handlebars");
const colorette = require("colorette");
const get_port_please_1 = require("get-port-please");
const fs_1 = require("fs");
const path = require("path");
const server_1 = require("./server");
const miscellaneous_1 = require("../../../utils/miscellaneous");
function getPageHTML(htmlTemplate, redocOptions = {}, useRedocPro, wsPort, host) {
    let templateSrc = (0, fs_1.readFileSync)(htmlTemplate, 'utf-8');
    // fix template for backward compatibility
    templateSrc = templateSrc
        .replace(/{?{{redocHead}}}?/, '{{{redocHead}}}')
        .replace('{{redocBody}}', '{{{redocHTML}}}');
    const template = (0, handlebars_1.compile)(templateSrc);
    return template({
        redocHead: `
  <script>
    window.__REDOC_EXPORT = '${useRedocPro ? 'RedoclyReferenceDocs' : 'Redoc'}';
    window.__OPENAPI_CLI_WS_PORT = ${wsPort};
    window.__OPENAPI_CLI_WS_HOST = "${host}";
  </script>
  <script src="/simplewebsocket.min.js"></script>
  <script src="/hot.js"></script>
  <script src="${useRedocPro
                ? 'patched-redocly-reference-docs.min.js'
                : 'https://cdn.redoc.ly/redoc/latest/bundles/redoc.standalone.js'}"></script>
`,
        redocHTML: `
  <div id="redoc"></div>
  <script>
    var container = document.getElementById('redoc');
    ${useRedocPro
                ? "window[window.__REDOC_EXPORT].setPublicPath('https://cdn.redoc.ly/reference-docs/latest/');"
                : ''}
    window[window.__REDOC_EXPORT].init("/openapi.json", ${JSON.stringify(redocOptions)}, container)
  </script>`,
    });
}
function startPreviewServer(port, host, { getBundle, getOptions, useRedocPro, }) {
    return __awaiter(this, void 0, void 0, function* () {
        const defaultTemplate = path.join(__dirname, 'default.hbs');
        const handler = (request, response) => __awaiter(this, void 0, void 0, function* () {
            var _a;
            console.time(colorette.dim(`GET ${request.url}`));
            const { htmlTemplate } = getOptions() || {};
            if (((_a = request.url) === null || _a === void 0 ? void 0 : _a.endsWith('/')) || path.extname(request.url) === '') {
                (0, server_1.respondWithGzip)(getPageHTML(htmlTemplate || defaultTemplate, getOptions(), useRedocPro, wsPort, host), request, response, {
                    'Content-Type': 'text/html',
                });
            }
            else if (request.url === '/openapi.json') {
                const bundle = yield getBundle();
                if (bundle === undefined) {
                    (0, server_1.respondWithGzip)(JSON.stringify({
                        openapi: '3.0.0',
                        info: {
                            description: '<code> Failed to generate bundle: check out console output for more details </code>',
                        },
                        paths: {},
                    }), request, response, {
                        'Content-Type': 'application/json',
                    });
                }
                else {
                    (0, server_1.respondWithGzip)(JSON.stringify(bundle), request, response, {
                        'Content-Type': 'application/json',
                    });
                }
            }
            else {
                let filePath =
                    // eslint-disable-next-line @typescript-eslint/ban-ts-comment
                    // @ts-ignore
                    {
                        '/hot.js': path.join(__dirname, 'hot.js'),
                        '/oauth2-redirect.html': path.join(__dirname, 'oauth2-redirect.html'),
                        '/simplewebsocket.min.js': require.resolve('simple-websocket/simplewebsocket.min.js'),
                        '/patched-redocly-reference-docs.min.js': path.join(__dirname, 'patched-redocly-reference-docs.min.js'),
                    }[request.url || ''];
                if (!filePath) {
                    const basePath = htmlTemplate ? path.dirname(htmlTemplate) : process.cwd();
                    filePath = path.resolve(basePath, `.${request.url}`);
                    if (!(0, miscellaneous_1.isSubdir)(basePath, filePath)) {
                        (0, server_1.respondWithGzip)('404 Not Found', request, response, { 'Content-Type': 'text/html' }, 404);
                        console.timeEnd(colorette.dim(`GET ${request.url}`));
                        return;
                    }
                }
                const extname = String(path.extname(filePath)).toLowerCase();
                const contentType = server_1.mimeTypes[extname] || 'application/octet-stream';
                try {
                    (0, server_1.respondWithGzip)(yield fs_1.promises.readFile(filePath), request, response, {
                        'Content-Type': contentType,
                    });
                }
                catch (e) {
                    if (e.code === 'ENOENT') {
                        (0, server_1.respondWithGzip)('404 Not Found', request, response, { 'Content-Type': 'text/html' }, 404);
                    }
                    else {
                        (0, server_1.respondWithGzip)(`Something went wrong: ${e.code || e.message}...\n`, request, response, {}, 500);
                    }
                }
            }
            console.timeEnd(colorette.dim(`GET ${request.url}`));
        });
        const wsPort = yield (0, get_port_please_1.getPort)({ port: 32201, portRange: [32201, 32301], host });
        const server = (0, server_1.startHttpServer)(port, host, handler);
        server.on('listening', () => {
            process.stdout.write(`\n  🔎  Preview server running at ${colorette.blue(`http://${host}:${port}\n`)}`);
        });
        return (0, server_1.startWsServer)(wsPort, host);
    });
}
exports.default = startPreviewServer;
