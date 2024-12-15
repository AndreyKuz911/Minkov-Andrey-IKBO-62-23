import fs from 'fs';
import path from 'path';
import https from 'https';
import { exec } from 'child_process';

// Чтение package.json из npm-реестра без сторонних библиотек
const fetchPackageJson = (packageName) => {
    return new Promise((resolve, reject) => {
        console.log(`Fetching package.json for ${packageName} from the registry...`);
        const url = `https://registry.npmjs.org/${packageName}`;
        https.get(url, (res) => {
            if (res.statusCode !== 200) {
                reject(new Error(`Failed to fetch ${packageName}: ${res.statusCode}`));
                return;
            }
            let data = '';
            res.on('data', chunk => data += chunk);
            res.on('end', () => {
                try {
                    const packageJson = JSON.parse(data);
                    const latestVersion = packageJson['dist-tags'].latest;
                    resolve(packageJson.versions[latestVersion]);
                } catch (error) {
                    reject(new Error(`Failed to parse package.json for ${packageName}: ${error.message}`));
                }
            });
        }).on('error', reject);
    });
};

// Получение всех зависимостей из package.json
const getDependencies = (packageJson) => ({
    ...packageJson.dependencies,
    ...packageJson.devDependencies,
    ...packageJson.peerDependencies,
});

// Рекурсивное получение зависимостей
const getAllDependencies = async (packageName, depth, currentDepth = 0, dependenciesMap = {}, visited = new Set()) => {
    if (currentDepth > depth) return dependenciesMap;

    // Пропускаем обработанные пакеты
    if (visited.has(packageName)) {
        return dependenciesMap;
    }
    visited.add(packageName);

    try {
        const packageJson = await fetchPackageJson(packageName);
        const dependencies = getDependencies(packageJson);

        // Добавляем зависимости текущего пакета
        dependenciesMap[packageName] = Object.keys(dependencies);

        // Рекурсивно обрабатываем зависимости
        for (const dep of Object.keys(dependencies)) {
            await getAllDependencies(dep, depth, currentDepth + 1, dependenciesMap, visited);
        }
    } catch (error) {
        console.error(`Error processing ${packageName}: ${error.message}`);
    }

    return dependenciesMap;
};

// Генерация графа в формате DOT
const generateDotGraph = (dependenciesMap) => {
    let graph = 'digraph G {\n';

    for (const packageName in dependenciesMap) {
        graph += `  "${packageName}" [shape=box];\n`;
        dependenciesMap[packageName].forEach(dep => {
            graph += `  "${packageName}" -> "${dep}";\n`;
        });
    }

    graph += '}\n';
    return graph;
};

// Основная функция
const main = async () => {
    const args = process.argv.slice(2);
    if (args.length < 4) {
        console.error('Usage: node index.js <path_to_dot_tool> <package_name> <output_file> <max_depth>');
        process.exit(1);
    }

    const [dotToolPath, packageName, outputFile, depth] = args;
    const maxDepth = parseInt(depth, 10);

    try {
        console.log(`Processing ${packageName} at depth ${maxDepth}`);

        // Получаем зависимости
        const dependenciesMap = await getAllDependencies(packageName, maxDepth);

        // Генерируем DOT-граф
        const dotGraph = generateDotGraph(dependenciesMap);

        // Выводим результат на экран
        console.log(dotGraph);

        // Сохраняем результат в файл
        fs.writeFileSync(outputFile, dotGraph);

        // Визуализация с помощью Graphviz
        exec(`${dotToolPath} -Tpng ${outputFile} -o output.png`, (err, stdout, stderr) => {
            if (err) {
                console.error(`Error executing Graphviz: ${stderr}`);
                return;
            }
            console.log('Graph visualized and saved as output.png');
        });
    } catch (error) {
        console.error(`Error: ${error.message}`);
    }
};

main();
