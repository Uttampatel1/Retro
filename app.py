import streamlit as st
from rxnmapper import RXNMapper
from rdkit import Chem
from rdkit.Chem import Draw
from rdkit.Chem import rdChemReactions
from rdkit.Chem.Draw import rdMolDraw2D
from rdkit.Chem.Draw import IPythonConsole
from PIL import Image

# Function to draw chemical reaction
def draw_chemical_reaction(smiles, highlightByReactant=False, font_scale=0.5):
    rxn = rdChemReactions.ReactionFromSmarts(smiles, useSmiles=True)
    trxn = rdChemReactions.ChemicalReaction(rxn)
    # Move atom maps to be annotations
    for m in trxn.GetReactants():
        moveAtomMapsToNotes(m)
    for m in trxn.GetProducts():
        moveAtomMapsToNotes(m)
    d2d = rdMolDraw2D.MolDraw2DSVG(2000, 400)
    d2d.drawOptions().annotationFontScale = font_scale
    d2d.DrawReaction(trxn, highlightByReactant=highlightByReactant)

    d2d.FinishDrawing()

    return d2d.GetDrawingText()

# Function to move atom maps to notes
def moveAtomMapsToNotes(m):
    for at in m.GetAtoms():
        if at.GetAtomMapNum():
            at.SetProp("atomNote", str(at.GetAtomMapNum()))

# Main Streamlit app
def main():
    st.set_page_config(page_title="Chemical Reaction Viewer", page_icon="🔬")
    st.title("🧪 Chemical Reaction Image Viewer 🖼️")

    # User input for SMILES
    smiles_pr = st.text_input("🔬 Enter Product SMILES :", "")
    
    smiles_part = st.text_input("🔍 Enter SMILE parts (separate by dot(.)) :", "")

    smiles_input = smiles_pr + ">>" + smiles_part

    if smiles_pr and smiles_part:
        # Button to submit input
        if st.button("🚀 Generate Reaction Image"):
            # Check if input is provided
            if smiles_input:
                
                rxn_mapper = RXNMapper()
                smiles = smiles_input
                # Generate reaction image
                outputs = rxn_mapper.get_attention_guided_atom_maps([smiles])
                for out in outputs:
                    # Save image to a temporary file
                    with open("temp.svg", "w") as f:
                        f.write(draw_chemical_reaction(out['mapped_rxn'], highlightByReactant=True))
                    
                    # Display image and confidence
                    st.image("temp.svg", use_column_width=True)
                    st.write(f'🎉 Confidence: {out["confidence"]:.2f}')
            else:
                st.warning("⚠️ Please enter a valid SMILES.")

if __name__ == "__main__":
    main()
