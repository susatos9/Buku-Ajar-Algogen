#!/usr/bin/env python3
"""
Cycle Crossover (CX) Visualization
Creates detailed step-by-step graphics for Cycle crossover example
"""

import matplotlib.pyplot as plt
import matplotlib.patches as patches
import numpy as np

def create_cycle_crossover_visualization():
    """Create a comprehensive Cycle Crossover visualization"""
    
    # Create figure with subplots
    fig = plt.figure(figsize=(16, 14))
    
    # Data for the example
    parent1 = [1, 2, 3, 4, 5, 6, 7, 8, 9]
    parent2 = [5, 4, 6, 9, 2, 3, 7, 1, 8]
    
    # Step 1: Show original parents
    ax1 = plt.subplot(6, 1, 1)
    ax1.set_title('Step 1: Original Parents with Position Indices', fontsize=14, fontweight='bold')
    
    # Draw Parent 1
    for i, val in enumerate(parent1):
        rect = patches.Rectangle((i, 1), 1, 0.8, linewidth=2, 
                               edgecolor='black', facecolor='lightblue')
        ax1.add_patch(rect)
        ax1.text(i+0.5, 1.4, str(val), ha='center', va='center', 
                fontsize=12, fontweight='bold')
        ax1.text(i+0.5, 0.7, str(i), ha='center', va='center', 
                fontsize=10, style='italic')
    
    # Draw Parent 2
    for i, val in enumerate(parent2):
        rect = patches.Rectangle((i, 0), 1, 0.8, linewidth=2, 
                               edgecolor='black', facecolor='lightgreen')
        ax1.add_patch(rect)
        ax1.text(i+0.5, 0.4, str(val), ha='center', va='center', 
                fontsize=12, fontweight='bold')
        ax1.text(i+0.5, -0.3, str(i), ha='center', va='center', 
                fontsize=10, style='italic')
    
    ax1.text(-1, 1.4, 'Parent 1:', ha='right', va='center', fontweight='bold')
    ax1.text(-1, 0.4, 'Parent 2:', ha='right', va='center', fontweight='bold')
    ax1.text(-1, 0.7, 'Positions:', ha='right', va='center', fontsize=10, style='italic')
    ax1.text(-1, -0.3, 'Positions:', ha='right', va='center', fontsize=10, style='italic')
    
    ax1.set_xlim(-2, 10)
    ax1.set_ylim(-0.8, 2.2)
    ax1.set_aspect('equal')
    ax1.axis('off')
    
    # Step 2: Find first cycle
    ax2 = plt.subplot(6, 1, 2)
    ax2.set_title('Step 2: Find Cycle 1 (Starting from Position 0)', fontsize=14, fontweight='bold')
    
    # Find cycles
    def find_cycles(p1, p2):
        visited = [False] * len(p1)
        cycles = []
        
        for start in range(len(p1)):
            if not visited[start]:
                cycle = []
                current = start
                
                while not visited[current]:
                    visited[current] = True
                    cycle.append(current)
                    # Find where p2[current] appears in p1
                    val_at_current = p2[current]
                    current = p1.index(val_at_current)
                
                if cycle:
                    cycles.append(cycle)
        
        return cycles
    
    cycles = find_cycles(parent1, parent2)
    cycle1 = cycles[0] if cycles else []
    
    # Colors for different cycles
    colors = ['lightcoral', 'lightyellow', 'lightpink', 'lightcyan']
    
    # Draw Parent 1 with cycle highlighting
    for i, val in enumerate(parent1):
        cycle_idx = None
        for c_idx, cycle in enumerate(cycles):
            if i in cycle:
                cycle_idx = c_idx
                break
        color = colors[cycle_idx % len(colors)] if cycle_idx is not None else 'lightgray'
        
        rect = patches.Rectangle((i, 1), 1, 0.8, linewidth=2, 
                               edgecolor='black', facecolor=color)
        ax2.add_patch(rect)
        ax2.text(i+0.5, 1.4, str(val), ha='center', va='center', 
                fontsize=12, fontweight='bold')
    
    # Draw Parent 2 with cycle highlighting
    for i, val in enumerate(parent2):
        cycle_idx = None
        for c_idx, cycle in enumerate(cycles):
            if i in cycle:
                cycle_idx = c_idx
                break
        color = colors[cycle_idx % len(colors)] if cycle_idx is not None else 'lightgray'
        
        rect = patches.Rectangle((i, 0), 1, 0.8, linewidth=2, 
                               edgecolor='black', facecolor=color)
        ax2.add_patch(rect)
        ax2.text(i+0.5, 0.4, str(val), ha='center', va='center', 
                fontsize=12, fontweight='bold')
    
    ax2.text(-1, 1.4, 'Parent 1:', ha='right', va='center', fontweight='bold')
    ax2.text(-1, 0.4, 'Parent 2:', ha='right', va='center', fontweight='bold')
    
    # Show cycle tracing
    cycle_text = []
    if cycle1:
        trace = []
        for i, pos in enumerate(cycle1):
            p1_val = parent1[pos]
            p2_val = parent2[pos]
            trace.append(f"Pos {pos}: P1={p1_val}, P2={p2_val}")
            
            # Draw arrows showing the cycle
            if i < len(cycle1) - 1:
                next_pos = cycle1[i + 1]
                ax2.annotate('', xy=(next_pos+0.5, 1.8), xytext=(pos+0.5, 1.8),
                           arrowprops=dict(arrowstyle='->', color='red', lw=2))
    
    # Add cycle explanation
    ax2.text(10, 1.5, 'Cycle 1 positions:', ha='left', va='center', fontweight='bold')
    ax2.text(10, 1.2, str(cycle1), ha='left', va='center')
    
    cycle_explanation = [
        "Start at pos 0: P1[0]=1, P2[0]=5",
        "Find 5 in P1: position 4",
        "At pos 4: P1[4]=5, P2[4]=2", 
        "Find 2 in P1: position 1",
        "At pos 1: P1[1]=2, P2[1]=4",
        "Find 4 in P1: position 3", 
        "At pos 3: P1[3]=4, P2[3]=9",
        "Find 9 in P1: position 8",
        "At pos 8: P1[8]=9, P2[8]=8",
        "Find 8 in P1: position 7",
        "At pos 7: P1[7]=8, P2[7]=1",
        "Find 1 in P1: position 0 (cycle complete)"
    ]
    
    for i, explanation in enumerate(cycle_explanation[:6]):
        ax2.text(10, 0.9-i*0.15, explanation, ha='left', va='center', fontsize=9)
    
    ax2.set_xlim(-2, 20)
    ax2.set_ylim(-0.5, 2.3)
    ax2.set_aspect('equal')
    ax2.axis('off')
    
    # Step 3: Show all cycles
    ax3 = plt.subplot(6, 1, 3)
    ax3.set_title('Step 3: Identify All Cycles', fontsize=14, fontweight='bold')
    
    # Draw all cycles with different colors
    for i, val in enumerate(parent1):
        cycle_idx = None
        for c_idx, cycle in enumerate(cycles):
            if i in cycle:
                cycle_idx = c_idx
                break
        color = colors[cycle_idx % len(colors)] if cycle_idx is not None else 'lightgray'
        
        rect = patches.Rectangle((i, 1), 1, 0.8, linewidth=2, 
                               edgecolor='black', facecolor=color)
        ax3.add_patch(rect)
        ax3.text(i+0.5, 1.4, str(val), ha='center', va='center', 
                fontsize=12, fontweight='bold')
    
    for i, val in enumerate(parent2):
        cycle_idx = None
        for c_idx, cycle in enumerate(cycles):
            if i in cycle:
                cycle_idx = c_idx
                break
        color = colors[cycle_idx % len(colors)] if cycle_idx is not None else 'lightgray'
        
        rect = patches.Rectangle((i, 0), 1, 0.8, linewidth=2, 
                               edgecolor='black', facecolor=color)
        ax3.add_patch(rect)
        ax3.text(i+0.5, 0.4, str(val), ha='center', va='center', 
                fontsize=12, fontweight='bold')
    
    ax3.text(-1, 1.4, 'Parent 1:', ha='right', va='center', fontweight='bold')
    ax3.text(-1, 0.4, 'Parent 2:', ha='right', va='center', fontweight='bold')
    
    # Show all cycles
    ax3.text(10, 1.4, 'All Cycles:', ha='left', va='center', fontweight='bold')
    for i, cycle in enumerate(cycles):
        color_patch = patches.Rectangle((10, 1.1-i*0.3), 0.3, 0.2, 
                                      facecolor=colors[i % len(colors)], 
                                      edgecolor='black')
        ax3.add_patch(color_patch)
        ax3.text(10.4, 1.2-i*0.3, f'Cycle {i+1}: {cycle}', ha='left', va='center')
    
    ax3.set_xlim(-2, 18)
    ax3.set_ylim(-0.5, 2)
    ax3.set_aspect('equal')
    ax3.axis('off')
    
    # Step 4: Create Child 1
    ax4 = plt.subplot(6, 1, 4)
    ax4.set_title('Step 4: Create Child 1 (Alternate cycles: C1 from P1, C2 from P2, etc.)', 
                 fontsize=14, fontweight='bold')
    
    # Create child 1
    child1 = [0] * len(parent1)
    for cycle_idx, cycle in enumerate(cycles):
        source_parent = parent1 if cycle_idx % 2 == 0 else parent2
        for pos in cycle:
            child1[pos] = source_parent[pos]
    
    # Draw child 1
    for i, val in enumerate(child1):
        cycle_idx = None
        for c_idx, cycle in enumerate(cycles):
            if i in cycle:
                cycle_idx = c_idx
                break
        color = colors[cycle_idx % len(colors)] if cycle_idx is not None else 'lightgray'
        
        rect = patches.Rectangle((i, 0), 1, 0.8, linewidth=2, 
                               edgecolor='black', facecolor=color)
        ax4.add_patch(rect)
        ax4.text(i+0.5, 0.4, str(val), ha='center', va='center', 
                fontsize=12, fontweight='bold')
    
    ax4.text(-1, 0.4, 'Child 1:', ha='right', va='center', fontweight='bold')
    
    # Show source explanation
    ax4.text(10, 0.8, 'Source for each cycle:', ha='left', va='center', fontweight='bold')
    for i, cycle in enumerate(cycles):
        source = "Parent 1" if i % 2 == 0 else "Parent 2"
        ax4.text(10, 0.5-i*0.2, f'Cycle {i+1}: from {source}', ha='left', va='center')
    
    ax4.set_xlim(-2, 16)
    ax4.set_ylim(-0.5, 1.2)
    ax4.set_aspect('equal')
    ax4.axis('off')
    
    # Step 5: Create Child 2
    ax5 = plt.subplot(6, 1, 5)
    ax5.set_title('Step 5: Create Child 2 (Alternate cycles: C1 from P2, C2 from P1, etc.)', 
                 fontsize=14, fontweight='bold')
    
    # Create child 2
    child2 = [0] * len(parent1)
    for cycle_idx, cycle in enumerate(cycles):
        source_parent = parent2 if cycle_idx % 2 == 0 else parent1
        for pos in cycle:
            child2[pos] = source_parent[pos]
    
    # Draw child 2
    for i, val in enumerate(child2):
        cycle_idx = None
        for c_idx, cycle in enumerate(cycles):
            if i in cycle:
                cycle_idx = c_idx
                break
        color = colors[cycle_idx % len(colors)] if cycle_idx is not None else 'lightgray'
        
        rect = patches.Rectangle((i, 0), 1, 0.8, linewidth=2, 
                               edgecolor='black', facecolor=color)
        ax5.add_patch(rect)
        ax5.text(i+0.5, 0.4, str(val), ha='center', va='center', 
                fontsize=12, fontweight='bold')
    
    ax5.text(-1, 0.4, 'Child 2:', ha='right', va='center', fontweight='bold')
    
    # Show source explanation
    ax5.text(10, 0.8, 'Source for each cycle:', ha='left', va='center', fontweight='bold')
    for i, cycle in enumerate(cycles):
        source = "Parent 2" if i % 2 == 0 else "Parent 1"
        ax5.text(10, 0.5-i*0.2, f'Cycle {i+1}: from {source}', ha='left', va='center')
    
    ax5.set_xlim(-2, 16)
    ax5.set_ylim(-0.5, 1.2)
    ax5.set_aspect('equal')
    ax5.axis('off')
    
    # Step 6: Final comparison
    ax6 = plt.subplot(6, 1, 6)
    ax6.set_title('Step 6: Final Result Comparison', fontsize=14, fontweight='bold')
    
    # Draw all chromosomes for comparison
    chromosomes = [
        ('Parent 1:', parent1, 'lightblue'),
        ('Parent 2:', parent2, 'lightgreen'),
        ('Child 1:', child1, 'lightyellow'),
        ('Child 2:', child2, 'lightpink')
    ]
    
    for row, (label, chromosome, color) in enumerate(chromosomes):
        for i, val in enumerate(chromosome):
            rect = patches.Rectangle((i, row), 1, 0.8, linewidth=2, 
                                   edgecolor='black', facecolor=color)
            ax6.add_patch(rect)
            ax6.text(i+0.5, row+0.4, str(val), ha='center', va='center', 
                    fontsize=12, fontweight='bold')
        
        ax6.text(-1, row+0.4, label, ha='right', va='center', fontweight='bold')
    
    # Add validation
    valid1 = len(set(child1)) == len(child1) == 9
    valid2 = len(set(child2)) == len(child2) == 9
    
    ax6.text(10, 3, 'Validation:', ha='left', va='center', fontweight='bold')
    ax6.text(10, 2.7, f'Child 1: {"✓ Valid" if valid1 else "✗ Invalid"}', 
             ha='left', va='center', color='green' if valid1 else 'red')
    ax6.text(10, 2.4, f'Child 2: {"✓ Valid" if valid2 else "✗ Invalid"}', 
             ha='left', va='center', color='green' if valid2 else 'red')
    
    # Add key property
    ax6.text(10, 2, 'Key Property:', ha='left', va='center', fontweight='bold')
    ax6.text(10, 1.7, 'Each element maintains its', ha='left', va='center')
    ax6.text(10, 1.4, 'position from one parent', ha='left', va='center')
    
    ax6.set_xlim(-2, 16)
    ax6.set_ylim(-0.5, 4.5)
    ax6.set_aspect('equal')
    ax6.axis('off')
    
    plt.tight_layout()
    plt.savefig('/media/nugroho-adi-susanto/Windows-SSD/Users/Nugroho Adi Susanto/Documents/UGM/Kuliah/ALGOGEN/drive-download-20250929T115349Z-1-001/latex-book/figures/cycle_crossover_detailed.png', 
                dpi=300, bbox_inches='tight')
    plt.savefig('/media/nugroho-adi-susanto/Windows-SSD/Users/Nugroho Adi Susanto/Documents/UGM/Kuliah/ALGOGEN/drive-download-20250929T115349Z-1-001/latex-book/figures/cycle_crossover_detailed.pdf', 
                bbox_inches='tight')
    plt.show()

if __name__ == "__main__":
    create_cycle_crossover_visualization()