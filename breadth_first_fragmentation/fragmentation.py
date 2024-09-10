"""Fragmentation module"""

# AUTOGENERATED! DO NOT EDIT! File to edit: ../nbs/fragmentation.ipynb.

# %% auto 0
__all__ = ['count_dummies', 'get_size', 'replace_last', 'check_reconstruction', 'check_bond_no', 'fragment_recursive',
           'break_into_fragments_defragmo']

# %% ../nbs/fragmentation.ipynb 3
import sys
if '..' not in sys.path:
    sys.path.append('..')
import numpy as np
from rdkit import Chem
from copy import deepcopy
from rdkit.Chem import MolToSmiles, MolFromSmiles, BRICS
from .utilities import mol_from_smiles, mols_from_smiles

# %% ../nbs/fragmentation.ipynb 4
def count_dummies(mol:Chem.rdchem.Mol, # input molecule
                  )->int: # count of dummy atoms
    'Function to count dummy atoms.'
    count = 0
    for atom in mol.GetAtoms():
        if atom.GetAtomicNum() == 0:
            count += 1
    return count

# %% ../nbs/fragmentation.ipynb 10
def get_size(frag:Chem.rdchem.Mol, # input fragment
             )->int: # count of real atoms
    'Function to count real atoms.'
    dummies = count_dummies(frag)
    total_atoms = frag.GetNumAtoms()
    real_atoms = total_atoms - dummies
    return real_atoms

# %% ../nbs/fragmentation.ipynb 17
def replace_last(s:str, # the string (fragment) to which the dummy label * is to be replaced with another fragment
                 old:str, # the string from the fragment s to be replaced
                 new:str, # the string to replace the 'old' string in the fragment s
                 )->str: # the original string s with the replacement
    'Function to replace the last occuring dummy label with a fragment.'
    s_reversed = s[::-1]
    old_reversed = old[::-1]
    new_reversed = new[::-1]

    # Replace the first occurrence in the reversed string
    s_reversed = s_reversed.replace(old_reversed, new_reversed, 1)

    # Reverse the string back to original order
    return s_reversed[::-1]

# %% ../nbs/fragmentation.ipynb 23
def check_reconstruction(frags:list[str], # list of fragments in SMILES format
                         frag_1:str, # head/tail fragment in SMILES format
                         frag_2:str, # head/tail fragment in SMILES format
                         orig_smi, # original molecule in SMILES format
                         )->bool: # whether the original molecule was reconstructed
    'Function to test whether the original molecule has been reconstructed.'
    try:
        frags_test = frags.copy()
        frags_test.append(frag_1)
        frags_test.append(frag_2)
        frag_2_re = frags_test[-1]
        for i in range(len(frags_test)-1):
            frag_1_re = frags_test[-1*i-2]
            recomb = replace_last(frag_2_re, '*', frag_1_re.replace('*', '',1))
            recomb_canon = MolToSmiles(MolFromSmiles(Chem.CanonSmiles(recomb)),rootedAtAtom = 1)
            frag_2_re = recomb_canon
        orig_smi_canon = MolToSmiles(MolFromSmiles(Chem.CanonSmiles(orig_smi)),rootedAtAtom = 1)
        if recomb_canon == orig_smi_canon:
            return True
        else:
            return False
    except:
        return False

# %% ../nbs/fragmentation.ipynb 29
def check_bond_no(bonds:list, # the list of BRIC bonds locations
                  frags:list, # the list of fragments
                  frag_list_len:int, # the length of the fragment list
                  smi:str, # the smiles string of the molecule
                  verbose:int=0, # print fragmentation process, set verbose to 1
                  )->tuple: # a tuple containing the fragment list and a boolean value to indicate whether fragmentation is complete
    'This function checks if the molecule has less bonds than the limit of BRIC bonds.'
    if (len(bonds) <= frag_list_len):
        if verbose == 1:
            print('Final Fragment: ', smi)
        frags.append(MolToSmiles(MolFromSmiles(Chem.CanonSmiles(smi)), rootedAtAtom=1))
        fragComplete = True
        return frags, fragComplete
    else:
        fragComplete = False
        return frags, fragComplete

# %% ../nbs/fragmentation.ipynb 35
def fragment_recursive(mol_smi_orig:str, # the original smiles string of the molecule
                       mol_smi:str, # the smiles string of the molecule
                       frags:list, # the list of fragments
                       counter:int, # the counter for the recursion
                       frag_list_len:int, # the length of the fragment list
                       min_length:int=0, # the minimum number of atoms in a fragment
                       verbose:int=0, # print fragmentation process, set verbose to 1
                       )->list: # the list of fragments
    'This recursive function fragments a molecule using the DEFRAGMO fragmentation method.'
    fragComplete = False
    try:
        counter += 1
        mol = MolFromSmiles(mol_smi)
        bonds = list(BRICS.FindBRICSBonds(mol))

        # Check if the mol has less bonds than the limit of BRIC bonds
        frags, fragComplete = check_bond_no(bonds, frags, frag_list_len, mol_smi, verbose)
        if fragComplete:
            return frags

        idxs, labs = list(zip(*bonds))

        bond_idxs = []
        for a1, a2 in idxs:
            bond = mol.GetBondBetweenAtoms(a1, a2)
            bond_idxs.append(bond.GetIdx())

        order = np.argsort(bond_idxs).tolist()
        bond_idxs = [bond_idxs[i] for i in order]
        for bond in bond_idxs:
            broken = Chem.FragmentOnBonds(mol,
                                        bondIndices=[bond],
                                        dummyLabels=[(0, 0)])
            head, tail = Chem.GetMolFrags(broken, asMols=True)
            head_bric_bond_no = len(list(BRICS.FindBRICSBonds(head)))
            tail_bric_bond_no = len(list(BRICS.FindBRICSBonds(tail)))
            
            if head_bric_bond_no <= frag_list_len:
                head_smi = Chem.CanonSmiles(MolToSmiles(head))
                tail_smi = MolToSmiles(MolFromSmiles(Chem.CanonSmiles(MolToSmiles(tail))), rootedAtAtom=1)
                if check_reconstruction(frags, head_smi, tail_smi, mol_smi_orig) & (get_size(head) >= min_length):
                    if verbose == 1:
                        print('Head fragment: ', head_smi)
                        print('Recurse tail: ', tail_smi)
                    frags.append(head_smi)
                    fragComplete = fragment_recursive(mol_smi_orig, tail_smi, frags, counter, frag_list_len = 0, min_length=min_length, verbose=verbose)  
                    if fragComplete:
                        return frags
                # if reconstruction fails, and there is only one bond, then add the fragment to the fragment list
                elif (len(bond_idxs) == 1) & (get_size(MolFromSmiles(mol_smi)) >= min_length):
                    if verbose == 1:
                        print('Final Fragment: ', mol_smi)
                    frags.append(MolToSmiles(MolFromSmiles(Chem.CanonSmiles(mol_smi)), rootedAtAtom=1))
                    fragComplete = True
                    return frags
                elif bond == bond_idxs[-1]:
                    fragComplete = fragment_recursive(mol_smi_orig, MolToSmiles(MolFromSmiles(Chem.CanonSmiles(mol_smi)), rootedAtAtom=1), frags, counter, frag_list_len + 1, min_length=min_length, verbose=verbose)
                    if fragComplete:
                        return frags
            elif tail_bric_bond_no <= frag_list_len:
                tail_smi = Chem.CanonSmiles(MolToSmiles(tail))
                head_smi = MolToSmiles(MolFromSmiles(Chem.CanonSmiles(MolToSmiles(head))), rootedAtAtom=1)
                if check_reconstruction(frags, tail_smi, head_smi, mol_smi_orig) & (get_size(tail) >= min_length):
                    if verbose == 1:
                        print('Tail: ', tail_smi)
                        print('Recurse Head: ', head_smi)
                    frags.append(tail_smi)
                    fragComplete = fragment_recursive(mol_smi_orig, head_smi, frags, counter, frag_list_len = 0, min_length=min_length, verbose=verbose)  
                    if fragComplete:
                        return frags
                elif (len(bond_idxs) == 1) & (get_size(MolFromSmiles(mol_smi)) >= min_length):
                    if verbose == 1:
                        print('Final fragment: ', mol_smi)
                    frags.append(MolToSmiles(MolFromSmiles(Chem.CanonSmiles(mol_smi)), rootedAtAtom=1))
                    fragComplete = True
                    return frags
                elif bond == bond_idxs[-1]:
                    fragComplete = fragment_recursive(mol_smi_orig, MolToSmiles(MolFromSmiles(Chem.CanonSmiles(mol_smi)), rootedAtAtom=1), frags, counter, frag_list_len + 1, min_length=min_length, verbose=verbose)
                    if fragComplete:
                        return frags
    except Exception:
        pass

# %% ../nbs/fragmentation.ipynb 42
def break_into_fragments_defragmo(mol:Chem.rdchem.Mol, # the molecule object
                                  smi:str, # the smiles string of the molecule
                                  min_length: int=0, # the minimum number of atoms in a fragment
                                  verbose:int=0, # print fragmentation process, set verbose to 1
                                  )->tuple: # a tuple containing the original smiles, the fragmented smiles, and the number of fragments
    'This function breaks a molecule into fragments using the DEFRAGMO fragmentation method.'
    frags = []
    fragment_recursive(smi, smi, frags, 0, 0, min_length=min_length, verbose=verbose)

    # if no fragments are found
    if len(frags) == 0:
        return smi, np.nan, 0

    # if only one fragment is found
    if len(frags) == 1:
        return smi, smi, 1
    
    return smi, ' '.join(frags), len(frags)
