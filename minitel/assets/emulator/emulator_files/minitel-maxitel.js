"use strict"
/**
 * @file minitel
 * @author Frédéric BISSON <zigazou@free.fr>
 * @version 1.0
 * 
 * Create and run a Minitel emulation with its keyboard.
 */

/**
 * Create and run a Minitel emulation with its keyboard.
 *
 * @param {string} screenCanvasId Identifier of the canvas element which will
 *                                show the Minitel screen.
 * @param {boolean} color true if emulation is in color, false for b&w.
 * @param {number} speed 1200, 4800, 9600 bps or 0 for max speed.
 * @param {string} keyboardId Identifier of an HTML element which contains the
 *                            keyboard grid.
 * @param {string} bipId Identifier of the bip audio element.
 * @param {string} webSocketURL URL of the web socket to connect to.
 */
function minitel(screenCanvasId, color, speed, keyboardId, bipId, webSocketURL) {
    importHTML
        .install()
        .then(() => {
            const socket = new WebSocket(webSocketURL)
            const canvas = document.getElementById(screenCanvasId)
            const screen = new MinitelScreen(canvas)
            const keyboard = new Keyboard(document.getElementById(keyboardId))
            const bip = document.getElementById(bipId)

            new MinitelEmulator(canvas, keyboard, socket, bip).setColor(color)
                                                              .setRefresh(speed)
        })
}

var wsHost = location.host;
var wsProto = "ws";

if (wsHost == "maxitel.boraha.korfuri.fr") {
    wsProto = "wss";
}

if (wsHost == "127.0.0.1:8080") {
    wsHost = "127.0.0.1:3611";
}

minitel(
    "minitel-screen",
    false,
    9600,
    "miedit",
    "minitel-bip",
    wsProto + "://" + wsHost + "/ws"
)
