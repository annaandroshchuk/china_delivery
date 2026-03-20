from django import forms


class LeadForm(forms.Form):
    """Lead capture form with honeypot anti-spam field."""

    name = forms.CharField(
        label="Ім'я",
        max_length=120,
        widget=forms.TextInput(attrs={"placeholder": "Ваше ім'я", "autocomplete": "name"}),
    )
    phone = forms.CharField(
        label="Телефон",
        max_length=30,
        widget=forms.TextInput(attrs={"placeholder": "+38 (___) ___-__-__", "autocomplete": "tel", "type": "tel"}),
    )
    email = forms.EmailField(
        label="Email",
        required=False,
        widget=forms.EmailInput(attrs={"placeholder": "your@email.com", "autocomplete": "email"}),
    )
    form_location = forms.CharField(widget=forms.HiddenInput(), initial="hero")

    # UTM and tracking hidden fields
    utm_source = forms.CharField(required=False, widget=forms.HiddenInput())
    utm_medium = forms.CharField(required=False, widget=forms.HiddenInput())
    utm_campaign = forms.CharField(required=False, widget=forms.HiddenInput())
    utm_content = forms.CharField(required=False, widget=forms.HiddenInput())
    utm_term = forms.CharField(required=False, widget=forms.HiddenInput())
    gclid = forms.CharField(required=False, widget=forms.HiddenInput())
    fbclid = forms.CharField(required=False, widget=forms.HiddenInput())

    # Honeypot — must remain empty
    website = forms.CharField(
        required=False,
        widget=forms.TextInput(attrs={"tabindex": "-1", "autocomplete": "off"}),
    )

    def clean_name(self) -> str:
        name = self.cleaned_data.get("name", "").strip()
        if len(name) < 2:
            raise forms.ValidationError("Вкажіть ваше повне ім'я.")
        return name

    def clean_phone(self) -> str:
        phone = self.cleaned_data.get("phone", "").strip()
        digits = "".join(c for c in phone if c.isdigit())
        if len(digits) < 9:
            raise forms.ValidationError("Введіть коректний номер телефону.")
        return phone

    def clean(self) -> dict:
        cleaned = super().clean()
        if cleaned.get("website"):
            raise forms.ValidationError("Підозріла активність. Повторіть пізніше.")
        return cleaned
