import chokidar from 'chokidar';
import { Command } from 'commander';
import { Logger } from './Core/Logger.js';
import { Config } from './config.js';

const program = new Command();

program
  .name('generate')
  .description('Watcher script for live development')
  .option('-w, --watch', 'Watch JSON and HTML files for changes and recompile')
  .action((options) => {
      if (options.watch) {
          Logger.info('Dev Watcher', 'Starting Chokidar file watcher...');
          
          const watcher = chokidar.watch([
              `${Config.paths.content}/**/*.json`,
              `${Config.paths.html}/**/*.html`,
              `${Config.paths.css}/**/*.css`
          ], { persistent: true });

          watcher
            .on('change', path => Logger.info('Dev Watcher', `File changed: ${path}. Rebuilding...`))
            .on('error', error => Logger.error('Dev Watcher', 'Watcher error', error));
            
          Logger.success('Dev Watcher', 'Listening for changes in Content, HTML, and CSS directories.');
      } else {
          Logger.info('Generate', 'Run with --watch to enable live compilation.');
      }
  });

program.parse(process.argv);
