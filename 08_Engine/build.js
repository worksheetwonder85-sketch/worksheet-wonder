import { Command } from 'commander';
import { Engine } from './Core/Engine.js';
import { Logger } from './Core/Logger.js';

const program = new Command();

program
  .name('worksheet-wonder-engine')
  .description('CLI to generate Worksheet Wonder PDFs')
  .version('1.0.0');

program
  .command('alphabet <letter>')
  .description('Generate an Alphabet worksheet')
  .action(async (letter) => {
    try {
        Logger.info('CLI', `Triggered generation for Alphabet: ${letter}`);
        const engine = new Engine();
        await engine.initialize();
        await engine.compileAndExport('Alphabet', letter);
        Logger.success('CLI', `Finished generating Alphabet ${letter}.`);
    } catch (error) {
        console.error("FATAL BUILD ERROR:", error.message);
        process.exit(1);
    }
  });

program
  .command('numbers <number>')
  .description('Generate a Number worksheet')
  .action(async (number) => {
    // Similar implementation
    Logger.info('CLI', `Triggered generation for Number: ${number}`);
  });

program
  .command('shapes <shape>')
  .description('Generate a Shape worksheet')
  .action(async (shape) => {
    // Similar implementation
    Logger.info('CLI', `Triggered generation for Shape: ${shape}`);
  });

program.parse(process.argv);
