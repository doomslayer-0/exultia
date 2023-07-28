use rand::Rng;
use std::cmp::Ordering;
use std::io;

fn guessGame() {

    loop {
        
        println!("How many guesses do you want?");

        let mut guessAmount: u32;

        io::stdin()
                .read_line(&mut guessAmount);
                .expect("Could not read input");
        
    }

    for...

}

fn main() {
    println!("Guess the number!");

    let secret_number = rand::thread_rng().gen_range(1..=100);

    loop {
        println!("Please input your guess.");

        let mut guess = String::new();

        io::stdin()
            .read_line(&mut guess)
            .expect("Failed to read line");

       let guess: u32 = match guess.trim().parse() {
            Ok(num) => num,
            Err(_) => continue,
        };
        println!("You guessed: {guess}");

        match guess.cmp(&secret_number) {
            Ordering::Less => println!("Too small!"),
            Ordering::Greater => println!("Too big!"),
            Ordering::Equal => {
                println!("You win!");
                break;
            }
        }
    }
}
