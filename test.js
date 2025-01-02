const { spawn } = require('child_process');
const readline = require('readline');

// запускаем python-процесс
const pythonProcess = spawn('python', ['main.py']);

// настройка readline для чтения пользовательского ввода
const rl = readline.createInterface({
  input: process.stdin,
  output: process.stdout,
  stdio: 'inherit',
});

// обработка вывода от python
pythonProcess.stdout.on('data', (data) => {
  console.log(data.toString().trim());
});

// обработка ошибок python
pythonProcess.stderr.on('data', (data) => {
  console.error(`ошибка python: ${data}`);
});

// завершение python-процесса
pythonProcess.on('close', (code) => {
  console.log(`python завершился с кодом ${code}`);
});
