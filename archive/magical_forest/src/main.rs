use std::io;

mod scene;

#[derive(Debug, Clone)]
struct Tree {
    name: String,
    height: f64,
    magical_power: i32,
}

impl Tree {
    fn new(name: String, height: f64, magical_power: i32) -> Self {
        Self {
            name,
            height,
            magical_power,
        }
    }

    fn grow(&mut self, inches: f64) {
        self.height += inches;
        self.magical_power += 1;
    }

    fn display(&self) {
        println!("🌳 {} - Height: {:.1}m, Magical Power: {}",
                 self.name, self.height, self.magical_power);
    }
}

#[derive(Debug)]
enum ForestEvent {
    TreeGrowth,
    MagicalStorm,
    VisitorArrival,
}

fn main() {
    println!("🌲 Welcome to the Magical Forest! 🌲");
    println!("Let's practice Rust by managing your enchanted grove.\n");

    let mut trees = Vec::new();

    // Add some starter trees
    trees.push(Tree::new("Oak of Wisdom".to_string(), 15.0, 10));
    trees.push(Tree::new("Pine of Courage".to_string(), 12.0, 8));
    trees.push(Tree::new("Maple of Kindness".to_string(), 10.0, 6));

    loop {
        display_forest(&trees);

        println!("\nWhat would you like to do?");
        println!("1. Add a new tree");
        println!("2. Water a tree (make it grow)");
        println!("3. Check tree distances");
        println!("4. Exit");

        let mut choice = String::new();
        io::stdin().read_line(&mut choice).expect("Failed to read line");

        match choice.trim() {
            "1" => add_new_tree(&mut trees),
            "2" => water_tree(&mut trees),
            "3" => check_distances(&trees),
            "4" => break,
            _ => println!("Please choose 1-4"),
        }
    }

    println!("\nThanks for visiting the Magical Forest! 🌟");
}

fn display_forest(trees: &[Tree]) {
    println!("\n🌲 Your Magical Forest 🌲");
    for tree in trees {
        tree.display();
    }
}

fn add_new_tree(trees: &mut Vec<Tree>) {
    println!("What would you like to name your new tree?");
    let mut name = String::new();
    io::stdin().read_line(&mut name).expect("Failed to read line");

    let name = name.trim().to_string();
    if !name.is_empty() {
        trees.push(Tree::new(name, 5.0, 3));
        println!("🌱 New tree planted!");
    }
}

fn water_tree(trees: &mut Vec<Tree>) {
    if trees.is_empty() {
        println!("No trees to water!");
        return;
    }

    println!("Which tree would you like to water? (0-{})", trees.len() - 1);
    let mut choice = String::new();
    io::stdin().read_line(&mut choice).expect("Failed to read line");

    if let Ok(index) = choice.trim().parse::<usize>() {
        if index < trees.len() {
            trees[index].grow(2.0);
            println!("💧 Tree watered and grew! 🌱");
        } else {
            println!("Invalid tree number!");
        }
    } else {
        println!("Please enter a valid number!");
    }
}

fn check_distances(trees: &[Tree]) {
    if trees.len() < 2 {
        println!("Need at least 2 trees to check distances!");
        return;
    }

    println!("\n📏 Tree Distances:");
    for i in 0..trees.len() {
        for j in (i + 1)..trees.len() {
            let distance = calculate_distance(trees[i].height, trees[j].height);
            println!("{} ↔ {}: {:.1} units apart",
                     trees[i].name, trees[j].name, distance);
        }
    }
}

fn calculate_distance(height1: f64, height2: f64) -> f64 {
    (height1 - height2).abs()
}

fn process_trees(trees: &[Tree]) -> Vec<String> {
    trees
        .iter()
        .filter(|tree| tree.magical_power > 5)
        .map(|tree| format!("Powerful {}", tree.name))
        .collect()
}
