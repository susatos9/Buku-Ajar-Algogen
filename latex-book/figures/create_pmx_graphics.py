#!/usr/bin/env python3
"""
PMX (Partially Mapped Crossover) Visualization
Creates detailed step-by-step graphics for PMX crossover example
"""

import matplotlib.pyplot as plt
import matplotlib.patches as patches
import numpy as np

def create_pmx_visualization():
    """Create a comprehensive PMX crossover visualization"""
    
    # Create figure with subplots
    fig = plt.figure(figsize=(16, 12))
    
    # Data for the example
    parent1 = [1, 2, 3, 4, 5, 6, 7, 8, 9]
    parent2 = [5, 4, 6, 9, 2, 3, 7, 1, 8]
    
    # Crossover points (indices 2-4, values at positions 2,3,4)
    cut1, cut2 = 2, 5
    
    # Step 1: Show original parents
    ax1 = plt.subplot(5, 1, 1)
    ax1.set_title('Step 1: Original Parents', fontsize=14, fontweight='bold')
    
    # Draw Parent 1
    for i, val in enumerate(parent1):
        color = 'lightcoral' if cut1 <= i < cut2 else 'lightblue'
        rect = patches.Rectangle((i, 1), 1, 0.8, linewidth=2, 
                               edgecolor='black', facecolor=color)
        ax1.add_patch(rect)
        ax1.text(i+0.5, 1.4, str(val), ha='center', va='center', 
                fontsize=12, fontweight='bold')
    
    # Draw Parent 2
    for i, val in enumerate(parent2):
        color = 'lightcoral' if cut1 <= i < cut2 else 'lightgreen'
        rect = patches.Rectangle((i, 0), 1, 0.8, linewidth=2, 
                               edgecolor='black', facecolor=color)
        ax1.add_patch(rect)
        ax1.text(i+0.5, 0.4, str(val), ha='center', va='center', 
                fontsize=12, fontweight='bold')
    
    ax1.text(-1, 1.4, 'Parent 1:', ha='right', va='center', fontweight='bold')
    ax1.text(-1, 0.4, 'Parent 2:', ha='right', va='center', fontweight='bold')
    
    # Add cut point indicators
    ax1.axvline(x=cut1, color='red', linestyle='--', linewidth=2)
    ax1.axvline(x=cut2, color='red', linestyle='--', linewidth=2)
    ax1.text(cut1, 2.2, 'Cut 1', ha='center', color='red', fontweight='bold')
    ax1.text(cut2, 2.2, 'Cut 2', ha='center', color='red', fontweight='bold')
    
    ax1.set_xlim(-2, 10)
    ax1.set_ylim(-0.5, 2.5)
    ax1.set_aspect('equal')
    ax1.axis('off')
    
    # Step 2: Show mapping
    ax2 = plt.subplot(5, 1, 2)
    ax2.set_title('Step 2: Create Mapping from Selected Segments', fontsize=14, fontweight='bold')
    
    # Selected segments
    p1_segment = parent1[cut1:cut2]  # [3, 4, 5]
    p2_segment = parent2[cut1:cut2]  # [6, 9, 2]
    
    # Draw mapping
    mapping_text = []
    for i, (p1_val, p2_val) in enumerate(zip(p1_segment, p2_segment)):
        mapping_text.append(f"{p1_val} ↔ {p2_val}")
        
        # Draw boxes for mapping
        rect1 = patches.Rectangle((i*2, 1), 1, 0.8, linewidth=2, 
                                edgecolor='black', facecolor='lightcoral')
        rect2 = patches.Rectangle((i*2, 0), 1, 0.8, linewidth=2, 
                                edgecolor='black', facecolor='lightcoral')
        ax2.add_patch(rect1)
        ax2.add_patch(rect2)
        
        ax2.text(i*2+0.5, 1.4, str(p1_val), ha='center', va='center', 
                fontsize=12, fontweight='bold')
        ax2.text(i*2+0.5, 0.4, str(p2_val), ha='center', va='center', 
                fontsize=12, fontweight='bold')
        
        # Draw mapping arrow
        ax2.annotate('', xy=(i*2+0.5, 0.8), xytext=(i*2+0.5, 1),
                    arrowprops=dict(arrowstyle='<->', color='red', lw=2))
    
    ax2.text(-1, 1.4, 'P1 segment:', ha='right', va='center', fontweight='bold')
    ax2.text(-1, 0.4, 'P2 segment:', ha='right', va='center', fontweight='bold')
    
    # Add mapping text
    ax2.text(8, 1, 'Mapping:', ha='left', va='center', fontweight='bold', fontsize=12)
    for i, text in enumerate(mapping_text):
        ax2.text(8, 0.7-i*0.3, text, ha='left', va='center', fontsize=11)
    
    ax2.set_xlim(-2, 12)
    ax2.set_ylim(-0.5, 2)
    ax2.set_aspect('equal')
    ax2.axis('off')
    
    # Step 3: Exchange segments
    ax3 = plt.subplot(5, 1, 3)
    ax3.set_title('Step 3: Exchange Segments Between Parents', fontsize=14, fontweight='bold')
    
    # Create initial children with exchanged segments
    child1_temp = parent1.copy()
    child1_temp[cut1:cut2] = parent2[cut1:cut2]
    
    for i, val in enumerate(child1_temp):
        color = 'lightcoral' if cut1 <= i < cut2 else 'lightblue'
        rect = patches.Rectangle((i, 0), 1, 0.8, linewidth=2, 
                               edgecolor='black', facecolor=color)
        ax3.add_patch(rect)
        ax3.text(i+0.5, 0.4, str(val), ha='center', va='center', 
                fontsize=12, fontweight='bold')
    
    ax3.text(-1, 0.4, 'Child 1 (temp):', ha='right', va='center', fontweight='bold')
    
    # Highlight conflicts
    conflicts = []
    for i in range(len(child1_temp)):
        if i < cut1 or i >= cut2:  # Outside the exchanged segment
            if child1_temp[i] in p2_segment:
                conflicts.append(i)
                # Highlight conflict with red border
                rect = patches.Rectangle((i, 0), 1, 0.8, linewidth=3, 
                                       edgecolor='red', facecolor='yellow', alpha=0.7)
                ax3.add_patch(rect)
    
    ax3.text(10, 0.8, 'Conflicts (duplicates):', ha='left', va='center', 
             fontweight='bold', color='red')
    ax3.text(10, 0.4, f'Positions: {conflicts}', ha='left', va='center', color='red')
    
    ax3.set_xlim(-2, 15)
    ax3.set_ylim(-0.5, 1.5)
    ax3.set_aspect('equal')
    ax3.axis('off')
    
    # Step 4: Resolve conflicts using mapping
    ax4 = plt.subplot(5, 1, 4)
    ax4.set_title('Step 4: Resolve Conflicts Using Mapping', fontsize=14, fontweight='bold')
    
    # Create mapping dictionary
    mapping = {}
    for p1_val, p2_val in zip(p1_segment, p2_segment):
        mapping[p1_val] = p2_val
        mapping[p2_val] = p1_val
    
    # Resolve conflicts
    child1_final = child1_temp.copy()
    resolution_steps = []
    
    for i in range(len(child1_final)):
        if i < cut1 or i >= cut2:  # Outside the exchanged segment
            original_val = child1_final[i]
            current_val = original_val
            
            # Keep mapping until we find a value not in the exchanged segment
            steps = [current_val]
            while current_val in p2_segment:
                current_val = mapping[current_val]
                steps.append(current_val)
                if len(steps) > 10:  # Safety break
                    break
            
            if original_val != current_val:
                child1_final[i] = current_val
                resolution_steps.append(f"Pos {i}: {original_val} → {current_val}")
    
    # Draw final child
    for i, val in enumerate(child1_final):
        color = 'lightcoral' if cut1 <= i < cut2 else 'lightgreen'
        rect = patches.Rectangle((i, 0), 1, 0.8, linewidth=2, 
                               edgecolor='black', facecolor=color)
        ax4.add_patch(rect)
        ax4.text(i+0.5, 0.4, str(val), ha='center', va='center', 
                fontsize=12, fontweight='bold')
    
    ax4.text(-1, 0.4, 'Child 1 (final):', ha='right', va='center', fontweight='bold')
    
    # Show resolution steps
    ax4.text(10, 0.8, 'Resolution steps:', ha='left', va='center', fontweight='bold')
    for i, step in enumerate(resolution_steps):
        ax4.text(10, 0.5-i*0.2, step, ha='left', va='center', fontsize=10)
    
    ax4.set_xlim(-2, 16)
    ax4.set_ylim(-0.5, 1.2)
    ax4.set_aspect('equal')
    ax4.axis('off')
    
    # Step 5: Final comparison
    ax5 = plt.subplot(5, 1, 5)
    ax5.set_title('Step 5: Final Result Comparison', fontsize=14, fontweight='bold')
    
    # Draw all chromosomes for comparison
    chromosomes = [
        ('Parent 1:', parent1, 'lightblue'),
        ('Parent 2:', parent2, 'lightgreen'),
        ('Child 1:', child1_final, 'lightyellow')
    ]
    
    for row, (label, chromosome, color) in enumerate(chromosomes):
        for i, val in enumerate(chromosome):
            rect = patches.Rectangle((i, row), 1, 0.8, linewidth=2, 
                                   edgecolor='black', facecolor=color)
            ax5.add_patch(rect)
            ax5.text(i+0.5, row+0.4, str(val), ha='center', va='center', 
                    fontsize=12, fontweight='bold')
        
        ax5.text(-1, row+0.4, label, ha='right', va='center', fontweight='bold')
    
    # Add validation
    validation_text = "✓ Valid permutation: " + ("Yes" if len(set(child1_final)) == len(child1_final) == 9 else "No")
    ax5.text(10, 1.5, validation_text, ha='left', va='center', fontweight='bold', 
             color='green' if len(set(child1_final)) == 9 else 'red')
    
    ax5.set_xlim(-2, 15)
    ax5.set_ylim(-0.5, 3.5)
    ax5.set_aspect('equal')
    ax5.axis('off')
    
    plt.tight_layout()
    plt.savefig('/media/nugroho-adi-susanto/Windows-SSD/Users/Nugroho Adi Susanto/Documents/UGM/Kuliah/ALGOGEN/drive-download-20250929T115349Z-1-001/latex-book/figures/pmx_crossover_detailed.png', 
                dpi=300, bbox_inches='tight')
    plt.savefig('/media/nugroho-adi-susanto/Windows-SSD/Users/Nugroho Adi Susanto/Documents/UGM/Kuliah/ALGOGEN/drive-download-20250929T115349Z-1-001/latex-book/figures/pmx_crossover_detailed.pdf', 
                bbox_inches='tight')
    plt.show()

if __name__ == "__main__":
    create_pmx_visualization()