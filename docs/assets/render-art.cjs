/* Optional artwork export tool. It is not part of the Grok skill. */
const fs = require('node:fs/promises');
const path = require('node:path');
const sharp = require('sharp');

async function main() {
  const root = __dirname;
  const character = (await fs.readFile(path.join(root, 'peerboop-character.png'))).toString('base64');
  const files = ['desk-hero.svg', 'desk-social.svg', 'peerboop-avatar.svg'];
  for (const file of files) {
    const source = path.join(root, file);
    const layout = (await fs.readFile(source, 'utf8')).replace(/href="data:image\/png;base64,[A-Za-z0-9+/=]+"/g, `href="data:image/png;base64,${character}"`);
    await fs.writeFile(source, layout);
    const output = source.replace(/\.svg$/, '.png');
    await sharp(Buffer.from(layout)).png({ compressionLevel: 9 }).toFile(output);
    console.log(path.relative(process.cwd(), output));
  }
}

main().catch(error => { console.error(error.message); process.exitCode = 1; });
