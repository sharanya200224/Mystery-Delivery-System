# FastBox Delivery System

A logistics simulator for a fictional delivery company called FastBox. The system simulates one day of operations, assigning packages to delivery agents, calculating distances traveled, and generating performance reports.

## Features

- Parse warehouse, agent, and package data from JSON files
- Assign packages to the nearest agent based on Euclidean distance
- Simulate delivery routes from agent → warehouse → destination
- Calculate total distance traveled by each agent
- Compute efficiency metrics (distance per package delivered)
- Identify the most efficient agent
- Generate JSON reports with delivery statistics

## Requirements

- Python 3.6 or higher
- No external libraries required (uses only built-in modules: `json`, `math`, `typing`, `collections`)

## Installation

1. Clone or download this repository
2. Ensure you have Python installed on your system
3. No additional packages need to be installed

## File Structure
