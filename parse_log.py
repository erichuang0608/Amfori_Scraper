import json

def parse_log_file(log_file_path):
    print(f"Parsing log file: {log_file_path}")
    
    try:
        # Read the log file
        with open(log_file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Extract the JSON part
        if "Response Content:" not in content:
            raise Exception("No Response Content found in log file")
            
        json_str = content.split("Response Content:", 1)[1].strip()
        
        # Parse JSON
        data = json.loads(json_str)
        
        # Print the full JSON content
        print("\nParsed JSON content:")
        print(json.dumps(data, indent=2, ensure_ascii=False))
        
        # Save the parsed JSON to a new file
        output_file = log_file_path.replace('.log', '_parsed.json')
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2, ensure_ascii=False)
            
        print(f"\nSuccessfully parsed JSON and saved to: {output_file}")
        
        # Print key information
        print("\nKey information:")
        print(f"UUID: {data.get('uuid')}")
        print(f"Site amfori ID: {data.get('monitoredSite', {}).get('siteAmforiId')}")
        print(f"Site Name: {data.get('monitoredSite', {}).get('name')}")
        print(f"Local Name: {data.get('monitoredSite', {}).get('localName')}")
        print(f"Address: {data.get('monitoredSite', {}).get('address')}")
        print(f"Contact Email: {data.get('monitoredSite', {}).get('contactDetails', {}).get('emailAddress')}")
        print(f"Contact Phone: {data.get('monitoredSite', {}).get('contactDetails', {}).get('phoneNumber')}")
        print(f"Request Date: {data.get('requestDate')}")
        print(f"Monitoring ID: {data.get('monitoringId')}")
        print(f"Monitoring Type: {data.get('monitoringType')}")
        
        return data
        
    except FileNotFoundError:
        print(f"Log file not found: {log_file_path}")
        raise
    except json.JSONDecodeError as e:
        print(f"Failed to parse JSON: {str(e)}")
        print(f"JSON content: {json_str}")
        raise
    except Exception as e:
        print(f"Error processing log file: {str(e)}")
        raise

if __name__ == "__main__":
    # Parse the log file
    log_file = "api_response_57a05cff-9cfc-4273-91a8-5198c6c6810a.log"
    data = parse_log_file(log_file) 