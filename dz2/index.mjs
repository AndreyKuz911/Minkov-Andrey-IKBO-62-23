import fs from 'fs';
import path from 'path';
import yargs from 'yargs';
import { hideBin } from 'yargs/helpers';
import { exec } from 'child_process';

// Чтение package.json для пакета
const readPackageJson = (packageName) => {
    const packagePath = path.join('node_modules', packageName, 'package.json');
    console.log(`Looking for package.json at ${packagePath}`);  // Отладочная информация
    if (!fs.existsSync(packagePath)) {
        console.log(`No package.json found for ${packageName}`);  // Отладочная информация
        return null;
    }
    const packageJson = JSON.parse(fs.readFileSync(packagePath, 'utf-8'));
    return packageJson;
};

// Функция для получения зависимостей из package.json
const getDependencies = (packageJson) => {
    const dependencies = {
        ...packageJson.dependencies,
        ...packageJson.devDependencies,
        ...packageJson.peerDependencies,
    };
    return dependencies;
};

// Рекурсивное получение зависимостей с учетом максимальной глубины
const getAllDependencies = (packageName, depth, currentDepth = 0, dependenciesMap = {}) => {
    if (currentDepth > depth) return dependenciesMap;

    // Читаем package.json
    const packageJson = readPackageJson(packageName);
    if (!packageJson) return dependenciesMap;

    const dependencies = getDependencies(packageJson);

    // Добавляем зависимость в мапу
    if (!dependenciesMap[packageName]) {
        console.log(`Adding dependencies for ${packageName}`);  // Отладочная информация
        dependenciesMap[packageName] = Object.keys(dependencies);
    }

    // Рекурсивно добавляем зависимости для всех зависимостей текущего пакета
    for (const dep in dependencies) {
        if (!dependenciesMap[dep]) {
            console.log(`Recursively fetching dependencies for ${dep}`);  // Отладочная информация
            getAllDependencies(dep, depth, currentDepth + 1, dependenciesMap);
        }
    }

    return dependenciesMap;
};

// Генерация графа в формате DOT
const generateDotGraph = (dependenciesMap) => {
    let graph = 'digraph G {\n';

    // Добавляем узлы и рёбра для каждой зависимости
    for (const packageName in dependenciesMap) {
        graph += `  "${packageName}" [shape=box];\n`;
        dependenciesMap[packageName].forEach(dep => {
            graph += `  "${packageName}" -> "${dep}";\n`;
        });
    }

    graph += '}\n';
    return graph;
};

// Основная функция для работы программы
const main = async () => {
    const argv = yargs(hideBin(process.argv))
        .usage('Usage: node index.js <path_to_dot_tool> <package_name> <output_file> <max_depth>')
        .demandCommand(4, 'You need to specify all arguments')
        .argv;

    const dotToolPath = argv._[0];
    const packageName = argv._[1];
    const outputFile = argv._[2];
    const depth = parseInt(argv._[3], 10);

    try {
        console.log(`Processing ${packageName} at depth 0`);  // Отладочная информация

        // Получаем все зависимости
        const dependenciesMap = getAllDependencies(packageName, depth);

        // Генерируем граф в формате DOT
        const dotGraph = generateDotGraph(dependenciesMap);

        // Сохраняем граф в файл
        fs.writeFileSync(outputFile, dotGraph);

        // Визуализируем граф с помощью Graphviz
        exec(`"${dotToolPath}" -Tpng ${outputFile} -o output.png`, (err, stdout, stderr) => {
            if (err) {
                console.error(`Error executing Graphviz: ${stderr}`);
                return;
            }
            console.log(`Graph visualized and saved as output.png`);
        });
    } catch (error) {
        console.error(`Error: ${error.message}`);
    }
};

main();
