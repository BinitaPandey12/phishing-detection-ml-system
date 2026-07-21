import pandas as pd
import re
import os
from datetime import datetime
import warnings
warnings.filterwarnings('ignore')

def clean_sms_dataset(input_path, output_path):
    """
    Clean SMS Spam Detection dataset
    
    Args:
        input_path: Path to the input CSV file
        output_path: Path to save cleaned CSV
    
    Returns:
        cleaned_df: Cleaned DataFrame
    """
    
    # ── Step 1: Load dataset ─────────────────────────────
    print("Step 1: Loading dataset...")
    df = pd.read_csv(input_path, encoding='utf-8', on_bad_lines='skip')
    print(f"Original shape: {df.shape}")
    print(f"Columns: {df.columns.tolist()}")
    
    # ── Step 2: Check if data is already cleaned ──────────
    print("\nStep 2: Checking data format...")
    
    # If 'cleaned_message' exists and 'text' doesn't, data is already cleaned
    if 'cleaned_message' in df.columns and 'text' not in df.columns:
        print("✓ Data appears to be already cleaned (has 'cleaned_message' column)")
        print("✓ No cleaning needed, just saving...")
        
        # Create directory if it doesn't exist
        output_dir = os.path.dirname(output_path)
        if output_dir and not os.path.exists(output_dir):
            os.makedirs(output_dir, exist_ok=True)
            print(f"✓ Created directory: {output_dir}")
        
        # Save the file
        df.to_csv(output_path, index=False)
        print(f"✓ Saved to: {output_path}")
        
        # Statistics
        spam_count = len(df[df['label'] == 'spam'])
        ham_count = len(df[df['label'] == 'ham'])
        
        print(f"\nDataset statistics:")
        print(f"  Total: {len(df):,} messages")
        print(f"  Spam: {spam_count:,} ({spam_count/len(df)*100:.1f}%)")
        print(f"  Ham: {ham_count:,} ({ham_count/len(df)*100:.1f}%)")
        
        return df
    
    # ── Step 3: Text cleaning function (if raw data) ────
    print("\nStep 3: Cleaning text messages...")
    
    # Check which column contains the text
    text_column = 'text' if 'text' in df.columns else 'message' if 'message' in df.columns else df.columns[1]
    print(f"Using column '{text_column}' for text cleaning")
    
    def clean_text(text):
        """Clean SMS text by expanding abbreviations and fixing formatting"""
        if pd.isna(text):
            return ""
        
        text = str(text)
        
        # SMS abbreviations dictionary
        abbreviations = {
            'u': 'you', 'ur': 'your', 'r': 'are', 'y': 'why',
            'd': 'the', 'b': 'be', 'k': 'okay', 'c': 'see',
            'n': 'and', 'w': 'with', '2': 'to', '4': 'for',
            'b4': 'before', 'bc': 'because', 'cuz': 'because',
            'plz': 'please', 'pls': 'please', 'thx': 'thanks',
            'ty': 'thank you', 'yw': 'you welcome',
            'lol': 'laughing out loud', 'omg': 'oh my god',
            'btw': 'by the way', 'imo': 'in my opinion',
            'idk': 'i do not know', 'idc': 'i do not care',
            'tbh': 'to be honest', 'nvm': 'never mind',
            'brb': 'be right back', 'bbs': 'be back soon',
            'bbl': 'be back later', 'gtg': 'got to go',
            'g2g': 'got to go', 'cya': 'see you',
            'ttys': 'talk to you soon', 'ttyl': 'talk to you later',
            'omw': 'on my way', 'ily': 'i love you',
            'ilu': 'i love you', 'luv': 'love',
            'msg': 'message', 'txt': 'text', 'fav': 'favorite',
            'sec': 'second', 'mins': 'minutes', 'hrs': 'hours',
            'ppl': 'people', 'ya': 'you', 'yall': 'you all',
            'l8r': 'later', 'gr8': 'great', '2day': 'today',
            '2moro': 'tomorrow', '2nite': 'tonight', 'w8': 'wait'
        }
        
        # Expand abbreviations (longest first to avoid partial matches)
        for short, full in sorted(abbreviations.items(), key=lambda x: len(x[0]), reverse=True):
            text = re.sub(r'\b' + re.escape(short) + r'\b', full, text, flags=re.IGNORECASE)
        
        # Fix punctuation spacing
        text = re.sub(r'\s+([!?.])', r'\1', text)
        text = re.sub(r'([!?.])\s+', r'\1 ', text)
        
        # Remove extra spaces and repeated punctuation
        text = re.sub(r'\s+', ' ', text).strip()
        text = re.sub(r'([!?.])\1+', r'\1', text)
        text = re.sub(r'\.{2,}', '.', text)
        
        # Convert to lowercase
        text = text.lower()
        
        return text
    
    # Apply cleaning
    df['cleaned_message'] = df[text_column].apply(clean_text)
    print(f"✓ Cleaned {len(df):,} messages")
    
    # ── Step 4: Standardize labels ──────────────────────
    print("\nStep 4: Standardizing labels...")
    df['label'] = df['label'].str.lower()
    print(f"Label distribution:\n{df['label'].value_counts()}")
    
    # ── Step 5: Remove invalid messages ─────────────────
    print("\nStep 5: Removing invalid messages...")
    before = len(df)
    df = df[df['cleaned_message'].str.len() > 2].copy()
    df = df.dropna(subset=['cleaned_message'])
    print(f"Removed {before - len(df)} invalid messages")
    
    # ── Step 6: Remove duplicates ──────────────────────
    print("\nStep 6: Removing duplicates...")
    before = len(df)
    df = df.drop_duplicates(subset=['cleaned_message'])
    print(f"Removed {before - len(df)} duplicate messages")
    
    # ── Step 7: Final dataset ────────────────────────────
    print("\nStep 7: Creating final dataset...")
    final_df = df[['label', 'cleaned_message']].copy()
    
    # Statistics
    spam_count = len(final_df[final_df['label'] == 'spam'])
    ham_count = len(final_df[final_df['label'] == 'ham'])
    
    print(f"\nFinal dataset statistics:")
    print(f"  Total: {len(final_df):,} messages")
    print(f"  Spam: {spam_count:,} ({spam_count/len(final_df)*100:.1f}%)")
    print(f"  Ham: {ham_count:,} ({ham_count/len(final_df)*100:.1f}%)")
    
    # Create directory if it doesn't exist
    output_dir = os.path.dirname(output_path)
    if output_dir and not os.path.exists(output_dir):
        os.makedirs(output_dir, exist_ok=True)
        print(f"✓ Created directory: {output_dir}")
    
    # ── Step 8: Save cleaned dataset ────────────────────
    print(f"\nStep 8: Saving cleaned dataset...")
    final_df.to_csv(output_path, index=False)
    print(f"✓ Saved to: {output_path}")
    print(f"✓ Final shape: {final_df.shape}")
    
    # ── Step 9: Show sample ─────────────────────────────
    print("\n" + "="*60)
    print("SAMPLE OF CLEANED DATA:")
    print("="*60)
    print(final_df.head(10).to_string(index=False))
    print("="*60)
    print("✅ CLEANING COMPLETE!")
    
    return final_df


if __name__ == "__main__":
    # ── Configuration ──────────────────────────────────
    INPUT_PATH = "cleaned_sms_dataset.csv"  # Your input file
    OUTPUT_PATH = "cleaned_sms_dataset_final.csv"  # Save in current directory
    
    # ── Run cleaning pipeline ──────────────────────────
    cleaned_data = clean_sms_dataset(INPUT_PATH, OUTPUT_PATH)