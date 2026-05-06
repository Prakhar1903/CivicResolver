package com.example.complaintportal.ui.components

import androidx.appcompat.app.AppCompatDelegate
import androidx.compose.foundation.background
import androidx.compose.foundation.clickable
import androidx.compose.foundation.layout.*
import androidx.compose.foundation.shape.RoundedCornerShape
import androidx.compose.material.icons.Icons
import androidx.compose.material.icons.filled.ArrowDropDown
import androidx.compose.material.icons.filled.Language
import androidx.compose.material3.*
import androidx.compose.runtime.*
import androidx.compose.ui.Alignment
import androidx.compose.ui.Modifier
import androidx.compose.ui.draw.clip
import androidx.compose.ui.graphics.Color
import androidx.compose.ui.unit.dp
import androidx.compose.ui.unit.sp
import androidx.core.os.LocaleListCompat
import androidx.compose.ui.res.stringResource
import com.example.complaintportal.R

data class AppLanguage(val code: String, val displayName: String)

val indianLanguages = listOf(
    AppLanguage("en", "English"),
    AppLanguage("hi", "हिन्दी (Hindi)"),
    AppLanguage("bn", "বাংলা (Bengali)"),
    AppLanguage("te", "తెలుగు (Telugu)"),
    AppLanguage("mr", "मराठी (Marathi)"),
    AppLanguage("ta", "தமிழ் (Tamil)"),
    AppLanguage("ur", "اردو (Urdu)"),
    AppLanguage("gu", "ગુજરાતી (Gujarati)"),
    AppLanguage("kn", "ಕನ್ನಡ (Kannada)"),
    AppLanguage("ml", "മലയാളം (Malayalam)"),
    AppLanguage("or", "ଓଡ଼ିଆ (Odia)"),
    AppLanguage("pa", "ਪੰਜਾਬੀ (Punjabi)"),
    AppLanguage("as", "অসমীয়া (Assamese)")
)

@Composable
fun LanguageSelector(
    modifier: Modifier = Modifier,
    textColor: Color = MaterialTheme.colorScheme.onSurface,
    iconColor: Color = MaterialTheme.colorScheme.primary,
    backgroundColor: Color = MaterialTheme.colorScheme.surfaceVariant.copy(alpha = 0.5f)
) {
    var expanded by remember { mutableStateOf(false) }
    
    // Get current locale
    val currentLocales = AppCompatDelegate.getApplicationLocales()
    val currentLanguageCode = if (!currentLocales.isEmpty) {
        currentLocales.get(0)?.language ?: "en"
    } else {
        "en"
    }
    
    val selectedLanguage = indianLanguages.find { it.code == currentLanguageCode } 
        ?: indianLanguages.first()

    Box(modifier = modifier) {
        Row(
            modifier = Modifier
                .clip(RoundedCornerShape(12.dp))
                .background(backgroundColor)
                .clickable { expanded = true }
                .padding(horizontal = 12.dp, vertical = 8.dp),
            verticalAlignment = Alignment.CenterVertically
        ) {
            Icon(
                imageVector = Icons.Default.Language,
                contentDescription = stringResource(R.string.language),
                tint = iconColor,
                modifier = Modifier.size(18.dp)
            )
            Spacer(modifier = Modifier.width(6.dp))
            Text(
                text = selectedLanguage.displayName.substringBefore(" ("), // Show only native part if it has brackets
                fontSize = 14.sp,
                color = textColor,
                style = MaterialTheme.typography.labelLarge
            )
            Spacer(modifier = Modifier.width(2.dp))
            Icon(
                imageVector = Icons.Default.ArrowDropDown,
                contentDescription = null,
                tint = textColor,
                modifier = Modifier.size(18.dp)
            )
        }

        DropdownMenu(
            expanded = expanded,
            onDismissRequest = { expanded = false },
            modifier = Modifier.background(MaterialTheme.colorScheme.surface)
        ) {
            indianLanguages.forEach { language ->
                DropdownMenuItem(
                    text = { 
                        Text(
                            text = language.displayName,
                            color = if (language.code == selectedLanguage.code) 
                                MaterialTheme.colorScheme.primary 
                            else 
                                MaterialTheme.colorScheme.onSurface
                        ) 
                    },
                    onClick = {
                        expanded = false
                        if (language.code != selectedLanguage.code) {
                            AppCompatDelegate.setApplicationLocales(
                                LocaleListCompat.forLanguageTags(language.code)
                            )
                        }
                    }
                )
            }
        }
    }
}
