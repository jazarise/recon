const fs = require('fs');
const path = require('path');
const crypto = require('crypto');

const ALL_FILES_DIR = "e:/ReconX/allfiles";
const OUTPUT_DIR = "e:/ReconX/intelligence";

const CATEGORIES = {
    "Recon": ["subdomain", "asn", "dns", "crawl", "asset", "amass", "subfinder", "httpx"],
    "Web Scanning": ["nuclei", "dalfox", "fuzz", "dirb", "gobuster", "ffuf", "sqlmap"],
    "Cloud Security": ["aws", "azure", "gcp", "kubernetes", "docker", "s3", "boto3"],
    "API Security": ["graphql", "openapi", "swagger", "rest", "api"],
    "OSINT": ["phoneinfoga", "holehe", "social", "email", "osint"],
    "Exploitation": ["sqli", "ssrf", "xss", "bypass", "privesc", "exploit", "cve"],
    "AI Systems": ["agent", "planner", "reasoning", "llm", "openai", "anthropic", "langchain", "prompt"],
    "Reporting": ["report", "dashboard", "summary", "html", "pdf", "markdown", "jinja"],
    "Orchestration": ["workflow", "scheduler", "queue", "pipeline", "celery", "rabbitmq", "kafka", "airflow", "dag"],
    "Infrastructure": ["dockerfile", "runtime", "deploy", "config", "env", "terraform", "ansible"],
    "Plugin Systems": ["plugin", "registry", "adapter", "module", "extension"],
    "CTF Automation": ["ctf", "challenge", "solver", "pwn"],
    "Burp/MCP Integrations": ["burp", "mcp", "extension", "proxy"],
    "Intelligence/Correlation": ["graph", "relation", "risk", "score", "neo4j", "correlation"]
};

function getHash(content) {
    const normalized = content.replace(/\s+/g, '');
    return crypto.createHash('sha256').update(normalized, 'utf8').digest('hex');
}

function walkSync(dir, filelist) {
    let files = [];
    try {
        files = fs.readdirSync(dir);
    } catch (err) {
        return filelist;
    }
    
    filelist = filelist || [];
    files.forEach(function(file) {
        let filepath = path.join(dir, file);
        try {
            if (fs.statSync(filepath).isDirectory()) {
                filelist = walkSync(filepath, filelist);
            } else {
                filelist.push(filepath);
            }
        } catch (e) {}
    });
    return filelist;
}

function analyze() {
    if (!fs.existsSync(OUTPUT_DIR)){
        fs.mkdirSync(OUTPUT_DIR, { recursive: true });
    }

    let tool_inventory = [];
    let capability_matrix = { "Uncategorized": [] };
    for (let cat in CATEGORIES) {
        capability_matrix[cat] = [];
    }

    let file_hashes = {};
    let dependency_graph = { nodes: [], edges: [] };
    let execution_entrypoints = [];

    let allFiles = walkSync(ALL_FILES_DIR);
    let total_files = 0;

    allFiles.forEach(filepath => {
        total_files++;
        let filename = path.basename(filepath);
        let ext = path.extname(filename).toLowerCase();
        
        let content = '';
        try {
            content = fs.readFileSync(filepath, 'utf8');
        } catch (e) {
            return;
        }

        let h = getHash(content);
        if (!file_hashes[h]) file_hashes[h] = [];
        file_hashes[h].push(filepath);

        let content_lower = content.toLowerCase();
        let name_lower = filename.toLowerCase();

        let matched_categories = [];
        for (let cat in CATEGORIES) {
            for (let kw of CATEGORIES[cat]) {
                if (content_lower.includes(kw) || name_lower.includes(kw)) {
                    matched_categories.push(cat);
                    break;
                }
            }
        }

        if (matched_categories.length === 0) {
            matched_categories.push("Uncategorized");
        }

        let lang = ext ? ext : "unknown";

        let exec_type = "library";
        if (content.includes("if __name__ ==") || content.includes("def main") || content.includes("func main()") || [".sh", ".bash"].includes(ext)) {
            exec_type = "cli_entrypoint";
            execution_entrypoints.push({
                file: filename,
                path: filepath,
                type: "cli",
                language: lang
            });
        } else if (content_lower.includes("flask") || content_lower.includes("fastapi") || content_lower.includes("app.listen")) {
            exec_type = "api_server";
            execution_entrypoints.push({
                file: filename,
                path: filepath,
                type: "api",
                language: lang
            });
        }

        let deps = [];
        if (lang === ".py") {
            let importRegex = /^(?:import|from)\s+([a-zA-Z0-9_\.]+)/gm;
            let match;
            while ((match = importRegex.exec(content)) !== null) {
                deps.push(match[1]);
            }
        } else if (lang === ".go") {
            let importRegex = /"([^"]+)"/g;
            let match;
            while ((match = importRegex.exec(content)) !== null) {
                deps.push(match[1]);
            }
        }
        deps = [...new Set(deps)];

        tool_inventory.push({
            filename: filename,
            path: filepath,
            language: lang,
            purpose: `Matches categories: ${matched_categories.join(', ')}`,
            category: matched_categories,
            dependencies: deps,
            execution_type: exec_type,
            related_tools: []
        });

        matched_categories.forEach(cat => {
            capability_matrix[cat].push(filename);
        });

        if (deps.length > 0) {
            dependency_graph.nodes.push({ id: filename, group: lang });
            deps.forEach(d => {
                dependency_graph.edges.push({ source: filename, target: d });
            });
        }
    });

    let duplicate_map = [];
    for (let h in file_hashes) {
        if (file_hashes[h].length > 1) {
            duplicate_map.push({
                hash: h,
                count: file_hashes[h].length,
                files: file_hashes[h]
            });
        }
    }

    console.log(`Processed ${total_files} files.`);
    console.log(`Found ${duplicate_map.length} duplicate groups.`);

    fs.writeFileSync(path.join(OUTPUT_DIR, "tool_inventory.json"), JSON.stringify(tool_inventory, null, 2));
    fs.writeFileSync(path.join(OUTPUT_DIR, "capability_matrix.json"), JSON.stringify(capability_matrix, null, 2));
    fs.writeFileSync(path.join(OUTPUT_DIR, "duplicate_map.json"), JSON.stringify(duplicate_map, null, 2));
    fs.writeFileSync(path.join(OUTPUT_DIR, "dependency_graph.json"), JSON.stringify(dependency_graph, null, 2));
    fs.writeFileSync(path.join(OUTPUT_DIR, "execution_entrypoints.json"), JSON.stringify(execution_entrypoints, null, 2));

    console.log("Successfully generated JSON files in", OUTPUT_DIR);
}

analyze();
