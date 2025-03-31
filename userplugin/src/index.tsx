/*
 * Immune Typer Plugin for Vencord
 * Capitalizes the first letter of every word in outgoing messages.
*/

import { addMessagePreSendListener, removeMessagePreSendListener } from "@api/MessageEvents";
import definePlugin from "@utils/types";

function capitalize(input: string, separator: string): string {
    const output: string[] = [];
    const extensions = [".txt", ".jpg", ".png", ".lua"];
    const lines = input.split(/\r?\n/);

    for (const line of lines) {
        const capitalizedLine: string[] = [];
        const splitLine = line.split(separator);

        splitLine.forEach((word, i) => {
            if (word.startsWith("http://") || word.startsWith("https://") || word.startsWith("www.")) {
                capitalizedLine.push(word);
            } else if (extensions.some(ext => word.endsWith(ext))) {
                capitalizedLine.push(word);
            } else if (word) {
                const capitalized = word[0].toUpperCase() + word.slice(1);
                capitalizedLine.push(capitalized);
            }

            if (i < splitLine.length - 1) {
                capitalizedLine.push(separator);
            }
        });

        output.push(capitalizedLine.join(""));
    }

    return output.join("\n");
}

export default definePlugin({
    name: "ImmuneTyper",
    description: "Capitalizes the first letter of every word in outgoing messages.",
    authors: [{ name: "serotuko", id: 719111486127210547n }],

    async start() {
        this.preSend = addMessagePreSendListener((channelId, msg) => {
            let content = msg.content;
            content = capitalize(content, " ");
            content = capitalize(content, "_");
            content = capitalize(content, "-");
            content = capitalize(content, "\"");
            content = capitalize(content, "(");
            content = capitalize(content, ")");

            msg.content = content;
        });
    },

    stop() {
        removeMessagePreSendListener(this.preSend);
    }
});
